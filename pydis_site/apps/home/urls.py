from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import HomeView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
    path('wiki/', include('wiki.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
