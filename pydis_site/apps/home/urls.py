from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


app_name = 'home'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
    path('wiki/', include('wiki.urls')),
    path('', TemplateView.as_view(template_name='home/index.html'), name='home.index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
