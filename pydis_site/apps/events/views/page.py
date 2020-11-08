from typing import List

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView


class PageView(TemplateView):
    """Handles event pages showing."""

    def get_template_names(self) -> List[str]:
        """Get specific template names."""
        path: str = self.kwargs['path']
        page_path = settings.PAGES_PATH / path
        if page_path.is_dir():
            page_path = page_path / "_index.html"
            path = f"{path}/_index.html"
        else:
            page_path = settings.PAGES_PATH / f"{path}.html"
            path = f"{path}.html"

        if not page_path.exists():
            raise Http404

        return [f"events/{settings.PAGES_PATH.name}/path}"]
