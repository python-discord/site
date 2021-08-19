from django.urls import path

from .viewsets import LogView

app_name = 'staff'
urlpatterns = [
    path('bot/logs/<int:pk>/', LogView.as_view(), name="logs"),
]
