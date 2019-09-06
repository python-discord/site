from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .viewsets import LogView

app_name = 'staff'
urlpatterns = [
    path('bot/logs/<int:pk>/', LogView.as_view(), name="logs"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
