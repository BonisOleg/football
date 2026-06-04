from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

admin.site.index_title = "Панель керування"

urlpatterns = [
    path("healthz/", lambda request: HttpResponse("ok")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("src.tournaments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
