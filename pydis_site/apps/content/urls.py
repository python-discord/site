import typing
from pathlib import Path

from django_distill import distill_path

from . import utils, views

app_name = "content"


def __get_all_files(root: Path, folder: typing.Optional[Path] = None) -> list[str]:
    """Find all folders and markdown files recursively starting from `root`."""
    if not folder:
        folder = root

    results = []

    for item in folder.iterdir():
        name = item.relative_to(root).__str__().replace("\\", "/")

        if item.is_dir():
            results.append(name)
            results.extend(__get_all_files(root, item))
        else:
            path, extension = name.rsplit(".", maxsplit=1)
            if extension == "md":
                results.append(path)

    return results


DISTILL_RETURN = typing.Iterator[dict[str, str]]


def get_all_pages() -> DISTILL_RETURN:
    """Yield a dict of all page categories."""
    for location in __get_all_files(Path("pydis_site", "apps", "content", "resources")):
        yield {"location": location}


def get_all_tags() -> DISTILL_RETURN:
    """Return all tag names and groups in static builds."""
    groups = {None}
    for tag in utils.get_tags_static():
        groups.add(tag.group)
        yield {"location": (f"{tag.group}/" if tag.group else "") + tag.name}

    groups.remove(None)
    for group in groups:
        yield {"location": group}


urlpatterns = [
    distill_path("", views.PageOrCategoryView.as_view(), name='pages'),
    distill_path(
        "tags/<path:location>/",
        views.TagView.as_view(),
        name="tag",
        distill_func=get_all_tags
    ),
    distill_path(
        "<path:location>/",
        views.PageOrCategoryView.as_view(),
        name='page_category',
        distill_func=get_all_pages
    ),
]
