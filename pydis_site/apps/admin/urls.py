from django.contrib import admin
from django.urls import path


app_name = 'admin'
urlpatterns = (
    path('', admin.site.urls),
)
