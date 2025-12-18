from django.contrib import admin
from django.urls import include, path

from .schema import InternalSchemaView, ExternalSchemaView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/schema/external/", ExternalSchemaView.as_view(), name="schema-external"),
    path("api/schema/internal/", InternalSchemaView.as_view(), name="schema-internal"),

    path("api/v1/external/", include("apps.external_api.urls")),
    path("api/v1/internal/", include("apps.internal_api.urls")),
]
