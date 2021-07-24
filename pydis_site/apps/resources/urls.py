from django.urls import path

from pydis_site.apps.resources import views

app_name = "resources"
urlpatterns = [
    path("", views.resources.resource_view, name="index"),
    path("list/", views.ResourcesListView.as_view(), name="resources")
]
