from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_external(request):
    return Response({"ok": True, "scope": "external"})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def health_internal(request):
    return Response({"ok": True, "scope": "internal"})