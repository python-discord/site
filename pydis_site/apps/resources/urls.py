from django.urls import path

from pydis_site.apps.resources import views

app_name = "resources"
urlpatterns = [
    path("", views.ResourcesView.as_view(), name="index"),
    path("<str:type>/", views.ResourcesList.as_view(), name="resources")
]
