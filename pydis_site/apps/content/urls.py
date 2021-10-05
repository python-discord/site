import typing
from pathlib import Path

from django_distill import distill_path

from . import views

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


def get_all_pages() -> typing.Iterator[dict[str, str]]:
    """Yield a dict of all pag categories."""
    for location in __get_all_files(Path("pydis_site", "apps", "content", "resources")):
        yield {"location": location}


urlpatterns = [
    distill_path("", views.PageOrCategoryView.as_view(), name='pages'),
    distill_path(
        "<path:location>/",
        views.PageOrCategoryView.as_view(),
        name='page_category',
        distill_func=get_all_pages
    ),
]
