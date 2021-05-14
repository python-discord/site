from django.contrib import admin
from django.urls import include, path

from .views import HomeView, timeline

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', include('pydis_site.apps.redirect.urls')),
    path('admin/', admin.site.urls),
    path('resources/', include('pydis_site.apps.resources.urls')),
    path('pages/', include('pydis_site.apps.content.urls')),
    path('events/', include('pydis_site.apps.events.urls', namespace='events')),
    path('timeline/', timeline, name="timeline"),
]
