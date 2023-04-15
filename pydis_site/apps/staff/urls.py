from django.urls import path

from .views import LogView

app_name = 'staff'
urlpatterns = [
    path('bot/logs/<int:pk>/', LogView.as_view(), name="logs"),
]
