from django.urls import path

from pydis_site.apps.events.views import IndexView, PagesView

app_name = "events"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<path:path>/", PagesView.as_view(), name="page"),
]
