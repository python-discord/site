import typing
from pathlib import Path

from django_distill import distill_path

from pydis_site.apps.resources import views

app_name = "resources"


def get_all_resources() -> typing.Iterator[dict[str, str]]:
    """Yield a dict of all resource categories."""
    for category in Path("pydis_site", "apps", "resources", "resources").iterdir():
        yield {"category": category.name}


urlpatterns = [
    distill_path("", views.ResourcesView.as_view(), name="index"),
    distill_path(
        "<str:category>/",
        views.ResourcesListView.as_view(),
        name="resources",
        distill_func=get_all_resources
    ),
]
