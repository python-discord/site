from django.contrib import admin
from django.urls import include, path

from .views import HomeView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('resources/', include('pydis_site.apps.resources.urls')),
    path('events/', include('pydis_site.apps.events.urls', namespace='events')),
]
