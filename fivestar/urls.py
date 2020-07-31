from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from fivestar.settings import settings

# Root paths for all applications

main_url_patterns = [
    # api for dataverse
    path('api-five/v1/', include('api.urls', namespace='api'))
]

# Swagger endpoints configuration

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API", 
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

swagger_patterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = swagger_patterns + main_url_patterns

# Static files in debug mode needed to be reached by url parser.
# In production mode, files should be available under directory
# declared in settings.STATIC_URL and settings.MEDIA_URL

if settings.DEBUG:
    urlpatterns = urlpatterns + [
    ] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
