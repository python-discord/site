from django.urls import path

from .views import HomeView, timeline

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('timeline/', timeline, name="timeline"),
]
