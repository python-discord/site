from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django_hosts import reverse


urlpatterns = (
    path('', admin.site.urls),
)
