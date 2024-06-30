from django_distill import distill_path

from .views import TimelineView

app_name = "timeline"

urlpatterns = [
    distill_path("", TimelineView.as_view(), name="index"),
]
