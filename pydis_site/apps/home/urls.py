from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView


app_name = 'home'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home/index.html'), name='home.index'),
    path('admin/', admin.site.urls)
]
