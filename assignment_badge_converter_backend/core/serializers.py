from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .utils import unique_username_from_email

User = get_user_model()


class TenantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)


class TenantListSerializer(serializers.Serializer):
    tenants = TenantSerializer(many=True)


class TenantSelectSerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)

    def validate(self, attrs):
        tenant_id = attrs.get("tenant_id")
        name = attrs.get("name")
        if bool(tenant_id) == bool(name):
            raise serializers.ValidationError("Provide exactly one of tenant_id or name.")
        return attrs


class TenantUserListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()


class TenantUsersResponseSerializer(serializers.Serializer):
    viewer_role = serializers.CharField()
    tenant = TenantSerializer()
    users = TenantUserListItemSerializer(many=True)


class TenantInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=["student", "faculty", "admin"], default="student")


class TenantUserRoleUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["student", "faculty", "admin"])


class ChatStreamSerializer(serializers.Serializer):
    message = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.get("email")
        username = unique_username_from_email(email)
        return User.objects.create_user(username=username, password=password, **validated_data)


class SignUpResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
