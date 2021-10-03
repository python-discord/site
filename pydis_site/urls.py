from django.urls import include, path

from pydis_site import settings

urlpatterns = (
    path('', include('pydis_site.apps.home.urls', namespace='home')),
)

if not settings.env("STATIC_BUILD"):
    urlpatterns += (
        path('staff/', include('pydis_site.apps.staff.urls', namespace='staff')),
    )
