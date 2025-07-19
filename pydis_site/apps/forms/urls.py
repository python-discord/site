from django.urls import path

from .views import AdminView, IndexView


app_name = "forms"
urlpatterns = (
    path("admin", AdminView.as_view(), name="admin"),
    path("", IndexView.as_view(), name="index"),
)
