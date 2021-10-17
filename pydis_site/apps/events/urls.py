import typing
from pathlib import Path

from django_distill import distill_path

from pydis_site.apps.events.views import IndexView, PageView

app_name = "events"


def __get_all_files(root: Path, folder: typing.Optional[Path] = None) -> list[str]:
    """Find all folders and HTML files recursively starting from `root`."""
    if not folder:
        folder = root

    results = []

    for sub_folder in folder.iterdir():
        results.append(
            sub_folder.relative_to(root).__str__().replace("\\", "/").replace(".html", "")
        )

        if sub_folder.is_dir():
            results.extend(__get_all_files(root, sub_folder))

    return results


def get_all_events() -> typing.Iterator[dict[str, str]]:
    """Yield a dict of all event pages."""
    for file in __get_all_files(Path("pydis_site", "templates", "events", "pages")):
        yield {"path": file}


urlpatterns = [
    distill_path("", IndexView.as_view(), name="index"),
    distill_path("<path:path>/", PageView.as_view(), name="page", distill_func=get_all_events),
]
