from django_distill import distill_path

from pydis_site.apps.resources import views

app_name = "resources"
urlpatterns = [
    distill_path("", views.resources.ResourceView.as_view(), name="index"),
    distill_path("<resource_type>/", views.resources.ResourceView.as_view(), name="index"),
]
