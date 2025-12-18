from django.urls import path

from apps.common.views import health_internal

urlpatterns = [
    path("health/", health_internal),
]
