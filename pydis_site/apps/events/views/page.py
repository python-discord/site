from pathlib import Path
from typing import List

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

PAGES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "events", "pages")


class PageView(TemplateView):
    """Handles event pages showing."""

    def get_template_names(self) -> List[str]:
        """Get specific template names"""
        page_path = PAGES_PATH / self.kwargs['path']
        if page_path.exists() and page_path.is_dir():
            page_path = page_path.joinpath("_index.html")
            self.kwargs['path'] = f"{self.kwargs['path']}/_index.html"
        else:
            page_path = PAGES_PATH.joinpath(f"{self.kwargs['path']}.html")
            self.kwargs['path'] = f"{self.kwargs['path']}.html"

        if not page_path.exists():
            raise Http404

        return [self.kwargs['path']]
