from django.urls import path

app_name = 'forms'

from . import views

urlpatterns = [
    path('hello', views.hello)
]
