from django.urls import path
from django_distill import distill_path

from pydis_site.apps.events.views import IndexView, PageView

app_name = "events"
urlpatterns = [
    distill_path("", IndexView.as_view(), name="index"),
    path("<path:path>/", PageView.as_view(), name="page"),
]
