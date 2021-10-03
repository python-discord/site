import typing
from pathlib import Path

from django_distill import distill_path

from . import views

app_name = "content"


def __get_all_folders(root: Path, folder: typing.Optional[Path] = None) -> list[str]:
    """Find all folders recursively within `folder`."""
    if not folder:
        folder = root

    folders = []

    for sub_folder in folder.iterdir():
        if sub_folder.is_dir():
            folders.append(sub_folder.relative_to(root).__str__().replace("\\", "/"))
            folders.extend(__get_all_folders(root, sub_folder))

    return folders


def get_all_pages() -> typing.Iterator[dict[str, str]]:
    """Yield a dict of all pag categories."""
    for location in __get_all_folders(Path("pydis_site", "apps", "content", "resources")):
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
