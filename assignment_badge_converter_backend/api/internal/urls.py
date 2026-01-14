from django.urls import path

from core.views import health_internal

urlpatterns = [
    path("health/", health_internal),
]
