from django.contrib import admin
from django.urls import include, path
from django_distill import distill_path

from pydis_site import settings
from .views import HomeView, timeline

app_name = 'home'

NON_STATIC_PATTERNS = [
    path('', include('pydis_site.apps.redirect.urls')),
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
] if not settings.env("STATIC_BUILD") else []

urlpatterns = [
    distill_path('', HomeView.as_view(), name='home'),
    *NON_STATIC_PATTERNS,
    path('resources/', include('pydis_site.apps.resources.urls')),
    path('pages/', include('pydis_site.apps.content.urls')),
    path('events/', include('pydis_site.apps.events.urls', namespace='events')),
    distill_path('timeline/', timeline, name="timeline"),
]
