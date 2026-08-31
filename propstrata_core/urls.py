"""PropStrata Engine URL Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Mobile & Web REST API
    path("api/v1/", include("apps.api.urls")),
    # Web UI Pages
    path("", include("apps.properties.web_urls")),
    path("agencies/", include("apps.agencies.web_urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
