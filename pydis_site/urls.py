from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.urls import include, path


def robots_txt(request: WSGIRequest) -> HttpResponse:
    """Return an allow everything robots.txtfile."""
    return HttpResponse("User-agent: *\nAllow: /", headers={"Content-type": "text/plain"})


urlpatterns = (
    path('', include('pydis_site.apps.home.urls', namespace='home')),
    path('robots.txt', robots_txt),
    path('staff/', include('pydis_site.apps.staff.urls', namespace='staff')),
)
