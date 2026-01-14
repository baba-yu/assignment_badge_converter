from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import SignUpResponseSerializer, SignUpSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def health_external(request):
    return Response({"ok": True, "scope": "external"})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def health_internal(request):
    return Response({"ok": True, "scope": "internal"})


@extend_schema(request=SignUpSerializer, responses={201: SignUpResponseSerializer})
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_external(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(SignUpResponseSerializer(user).data, status=status.HTTP_201_CREATED)
