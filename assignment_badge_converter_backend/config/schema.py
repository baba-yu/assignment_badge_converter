from django.urls import get_resolver
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView


def _patterns_for(prefix: str):
    """
    prefix: "api/v1/external/" or "api/v1/internal/"
    """
    resolver = get_resolver()
    patterns = []
    for p in resolver.url_patterns:
        # p.pattern is RoutePattern; string化で確認
        if str(p.pattern).startswith(prefix):
            patterns.append(p)
    return patterns


class ExternalSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        self.patterns = _patterns_for("api/v1/external/")
        return super().get_schema(request=request, public=public)


class InternalSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        self.patterns = _patterns_for("api/v1/internal/")
        return super().get_schema(request=request, public=public)


class ExternalSchemaView(SpectacularAPIView):
    generator_class = ExternalSchemaGenerator


class InternalSchemaView(SpectacularAPIView):
    generator_class = InternalSchemaGenerator
