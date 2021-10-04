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

    for sub_folder in folder.iterdir():
        if sub_folder.is_dir():
            results.append(sub_folder.relative_to(root).__str__().replace("\\", "/"))
            results.extend(__get_all_files(root, sub_folder))
        else:
            path, extension = sub_folder.relative_to(root).__str__().rsplit(".", maxsplit=1)
            if extension == "md":
                results.append(path.replace("\\", "/"))

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
