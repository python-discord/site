from pathlib import Path

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.template import Context, Template
from django.views import View

PAGES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "events", "pages")


class PageView(View):
    """Handles event pages showing."""

    def get(self, request: WSGIRequest, path: str) -> HttpResponse:
        """Render event page rendering based on path."""
        # We need to get rid from trailing slash when path have this
        if path.endswith("/"):
            path = path[:-1]

        page_path = PAGES_PATH.joinpath(path)
        if page_path.exists() and page_path.is_dir():
            page_path = page_path.joinpath("_index.html")
        else:
            page_path = PAGES_PATH.joinpath(f"{path}.html")

        if not page_path.exists():
            raise Http404

        template = Template(page_path.read_text())
        return HttpResponse(template.render(Context()))
