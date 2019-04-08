from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


app_name = 'home'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('wiki/', include('wiki.urls')),
    path('', TemplateView.as_view(template_name='home/index.html'), name='index'),
]
