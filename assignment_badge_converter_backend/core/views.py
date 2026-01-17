import os

from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from openai import OpenAI

from .models import ChatMessage, Tenant, TenantUser, User
from .serializers import (
    ChatStreamSerializer,
    SignUpResponseSerializer,
    SignUpSerializer,
    TenantInviteSerializer,
    TenantUserListItemSerializer,
    TenantUserRoleUpdateSerializer,
    TenantUsersResponseSerializer,
    TenantListSerializer,
    TenantSelectSerializer,
    TenantSerializer,
)
from .utils import unique_username_from_email


@api_view(["GET"])
@permission_classes([AllowAny])
def health_external(request):
    return Response({"ok": True, "scope": "external"})


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email or not password:
            raise AuthenticationFailed("Email and password are required.")

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist as exc:
            raise AuthenticationFailed("No active account found with the given credentials.") from exc

        if not user.is_active or not user.check_password(password):
            raise AuthenticationFailed("No active account found with the given credentials.")

        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


@extend_schema(request=SignUpSerializer, responses={201: SignUpResponseSerializer})
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_external(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(SignUpResponseSerializer(user).data, status=status.HTTP_201_CREATED)


def _current_tenant_or_404(user):
    if not user.current_tenant:
        raise NotFound("Current tenant is not set.")
    if user.current_tenant.deleted_at:
        user.current_tenant = None
        user.save(update_fields=["current_tenant"])
        raise NotFound("Current tenant is not set.")
    return user.current_tenant


def _require_tenant_role(user, tenant, role):
    membership = TenantUser.objects.filter(tenant=tenant, user=user).first()
    if not membership:
        raise PermissionDenied("You do not belong to this tenant.")
    if membership.role != role:
        raise PermissionDenied("You do not have permission to perform this action.")
    return membership


def _get_membership(user, tenant):
    membership = TenantUser.objects.filter(tenant=tenant, user=user).first()
    if not membership:
        raise PermissionDenied("You do not belong to this tenant.")
    return membership


@extend_schema(request=TenantSelectSerializer, responses={200: TenantSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tenant_select_external(request):
    serializer = TenantSelectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tenant_id = serializer.validated_data.get("tenant_id")
    name = serializer.validated_data.get("name")

    if tenant_id:
        try:
            tenant = Tenant.objects.get(id=tenant_id, deleted_at__isnull=True)
        except Tenant.DoesNotExist as exc:
            raise NotFound("Tenant not found.") from exc
        if not TenantUser.objects.filter(tenant=tenant, user=request.user).exists():
            raise PermissionDenied("You do not belong to this tenant.")
    else:
        tenant = Tenant.objects.create(name=name)
        TenantUser.objects.create(tenant=tenant, user=request.user, role=TenantUser.ROLE_ADMIN)

    request.user.current_tenant = tenant
    request.user.save(update_fields=["current_tenant"])
    return Response(TenantSerializer(tenant).data)


@extend_schema(responses={200: TenantListSerializer})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tenant_list_external(request):
    tenant_ids = TenantUser.objects.filter(user=request.user).values_list("tenant_id", flat=True)
    tenants = Tenant.objects.filter(id__in=tenant_ids, deleted_at__isnull=True).order_by("name")
    payload = {"tenants": TenantSerializer(tenants, many=True).data}
    return Response(payload)


@extend_schema(responses={200: TenantUsersResponseSerializer})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tenant_users_external(request):
    tenant = _current_tenant_or_404(request.user)
    membership = _get_membership(request.user, tenant)
    memberships = (
        TenantUser.objects.filter(tenant=tenant)
        .select_related("user")
        .order_by("user__id")
    )
    users = [
        {
            "id": m.user.id,
            "email": m.user.email,
            "first_name": m.user.first_name,
            "last_name": m.user.last_name,
            "role": m.role,
        }
        for m in memberships
    ]
    payload = {"viewer_role": membership.role, "users": users}
    payload["tenant"] = TenantSerializer(tenant).data
    return Response(TenantUsersResponseSerializer(payload).data)


@extend_schema(request=TenantInviteSerializer, responses={201: TenantUserListItemSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tenant_invite_external(request):
    tenant = _current_tenant_or_404(request.user)
    _require_tenant_role(request.user, tenant, TenantUser.ROLE_ADMIN)

    serializer = TenantInviteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = User.objects.filter(email=data["email"]).first()
    if not user:
        username = unique_username_from_email(data["email"])
        user = User(
            username=username,
            email=data["email"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        user.set_unusable_password()
        user.save()

    if TenantUser.objects.filter(tenant=tenant, user=user).exists():
        return Response(
            {"detail": "User already belongs to this tenant."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    membership = TenantUser.objects.create(tenant=tenant, user=user, role=data["role"])
    payload = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": membership.role,
    }
    return Response(TenantUserListItemSerializer(payload).data, status=status.HTTP_201_CREATED)


@extend_schema(request=TenantUserRoleUpdateSerializer, responses={200: TenantUserListItemSerializer})
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def tenant_user_role_external(request, user_id: int):
    tenant = _current_tenant_or_404(request.user)
    _require_tenant_role(request.user, tenant, TenantUser.ROLE_ADMIN)

    serializer = TenantUserRoleUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        membership = TenantUser.objects.select_related("user").get(tenant=tenant, user_id=user_id)
    except TenantUser.DoesNotExist as exc:
        raise NotFound("User not found in tenant.") from exc

    membership.role = serializer.validated_data["role"]
    membership.save(update_fields=["role"])
    payload = {
        "id": membership.user.id,
        "email": membership.user.email,
        "first_name": membership.user.first_name,
        "last_name": membership.user.last_name,
        "role": membership.role,
    }
    return Response(TenantUserListItemSerializer(payload).data)


@extend_schema(responses={200: TenantSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tenant_delete_external(request, tenant_id: int):
    tenant = _current_tenant_or_404(request.user)
    if tenant.id != tenant_id:
        raise PermissionDenied("You do not have permission to perform this action.")
    _require_tenant_role(request.user, tenant, TenantUser.ROLE_ADMIN)

    if tenant.deleted_at:
        return Response({"detail": "Tenant already deleted."}, status=status.HTTP_400_BAD_REQUEST)

    tenant.deleted_at = timezone.now()
    tenant.save(update_fields=["deleted_at"])
    User.objects.filter(current_tenant=tenant).update(current_tenant=None)
    return Response(TenantSerializer(tenant).data)


@extend_schema(request=ChatStreamSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_stream_external(request):
    tenant = _current_tenant_or_404(request.user)
    _get_membership(request.user, tenant)

    serializer = ChatStreamSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.validated_data["message"]

    ChatMessage.objects.create(
        tenant=tenant,
        user=request.user,
        role=ChatMessage.ROLE_USER,
        content=message,
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise PermissionDenied("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        stream=True,
    )

    def event_stream():
        parts = []
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if not delta:
                continue
            parts.append(delta)
            yield delta
        full = "".join(parts).strip()
        if full:
            ChatMessage.objects.create(
                tenant=tenant,
                user=request.user,
                role=ChatMessage.ROLE_ASSISTANT,
                content=full,
            )

    return StreamingHttpResponse(event_stream(), content_type="text/plain")
