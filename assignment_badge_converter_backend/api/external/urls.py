from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import (
    EmailTokenObtainPairView,
    chat_stream_external,
    health_external,
    signup_external,
    tenant_invite_external,
    tenant_list_external,
    tenant_delete_external,
    tenant_select_external,
    tenant_user_role_external,
    tenant_users_external,
)

urlpatterns = [
    path("health/", health_external),
    path("auth/signup/", signup_external, name="auth_signup"),
    path("tenants/", tenant_list_external, name="tenant_list"),
    path("tenants/select/", tenant_select_external, name="tenant_select"),
    path("tenants/<int:tenant_id>/delete/", tenant_delete_external, name="tenant_delete"),
    path("tenants/users/", tenant_users_external, name="tenant_users"),
    path("tenants/users/invite/", tenant_invite_external, name="tenant_invite"),
    path("tenants/users/<int:user_id>/role/", tenant_user_role_external, name="tenant_user_role"),

    # JWT
    path("auth/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Chat
    path("chat/stream/", chat_stream_external, name="chat_stream"),
]
