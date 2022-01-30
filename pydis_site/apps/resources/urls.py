import typing

from django_distill import distill_path

from pydis_site.apps.resources import views

# This is only used for `distill_path`, so that the Netlify Deploy Previews
# can successfully redirect to static pages. This could probably be improved by
# making it less hardcoded, but since there's a bunch of special cases, and since
# it only affects deploy previews, I'm choosing to solve this with a simple solution.
VALID_RESOURCE_TYPES = [
    "book",
    "books",
    "reading",
    "podcast",
    "podcasts",
    "interactive",
    "videos",
    "video",
    "courses",
    "course",
    "communities",
    "community",
    "tutorial",
    "tutorials",
    "tool",
    "tools",
    "project ideas",
    "project-ideas",
]


def get_all_pages() -> typing.Iterator[dict[str, str]]:
    for resource_type in VALID_RESOURCE_TYPES:
        yield {"resource_type": resource_type}


app_name = "resources"
urlpatterns = [
    distill_path("", views.resources.ResourceView.as_view(), name="index"),
    distill_path(
        "<resource_type>/",
        views.resources.ResourceView.as_view(),
        name="index",
        distill_func=get_all_pages,
    ),
]
