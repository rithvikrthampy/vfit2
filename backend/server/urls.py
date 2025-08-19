from django.contrib import admin
from django.urls import path, include
from viewer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # pages
    path("", views.index, name="index"),
    path("viewer/", views.viewer, name="viewer"),

    # API endpoints
    path("api/shirts/", views.api_list_shirts, name="api_list_shirts"),
    path("api/run/", views.api_run_pix2surf, name="api_run_pix2surf"),
    path("api/run/<int:img_id>/", views.api_run, name="api_run_legacy"),  # legacy support
]

# dev static/media - serve from both frontend and backend
urlpatterns += static(settings.STATIC_URL, document_root=settings.FRONTEND_DIR / "static")
urlpatterns += static("/static/pix2surf/", document_root=settings.BASE_DIR / "pix2surf")
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static("/media/", document_root=settings.BASE_DIR / "data" / "media")
