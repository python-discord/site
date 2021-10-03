from django.urls import path
from django_distill import distill_path

from pydis_site.apps.resources import views

app_name = "resources"
urlpatterns = [
    distill_path("", views.ResourcesView.as_view(), name="index"),
    path("<str:category>/", views.ResourcesListView.as_view(), name="resources"),
]
