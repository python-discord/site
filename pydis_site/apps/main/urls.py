from django.contrib import admin
from django.urls import path

from .views import HomeView


app_name = 'main'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls)
]
