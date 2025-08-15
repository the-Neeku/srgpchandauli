from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("srgp-admin-dashboard/", admin.site.urls),
    path("", include("MAIN_APP.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
