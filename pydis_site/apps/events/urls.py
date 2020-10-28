from django.urls import path, re_path

from pydis_site.apps.events.views import IndexView, PageView

app_name = "events"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    re_path("(?P<path>.+)/$", PageView.as_view(), name="page"),
]
