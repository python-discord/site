from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .viewsets import LogView

app_name = 'staff'
urlpatterns = [
    path('bot/logs/<int:pk>/', LogView.as_view(), name="logs"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
