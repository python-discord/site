from django.contrib import admin
from django.urls import path

from .views import Home


app_name = 'home'
urlpatterns = [
    path('', Home.as_view(), name='home.index'),
    path('admin/', admin.site.urls)
]
