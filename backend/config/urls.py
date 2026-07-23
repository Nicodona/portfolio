from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import include, path, re_path
from django.views.static import serve


def spa_index(request, path=""):
    index = settings.FRONTEND_DIST / "index.html"
    if not index.exists():
        return HttpResponseNotFound(
            "Frontend build not found. In development use the Vite server "
            "on port 5173."
        )
    return HttpResponse(index.read_bytes(), content_type="text/html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("portfolio.urls")),
    # Media is a handful of images and one CV, so Django serving it directly
    # keeps the deployment to a single container.
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    # Everything else falls through to the React app (client side routing,
    # e.g. /stats). Static assets are handled by WhiteNoise before this.
    re_path(r"^(?P<path>(?!static/|assets/).*)$", spa_index),
]
