import typing as t
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from pydis_site.apps.content import utils


class PageOrCategoryView(TemplateView):
    """Handles pages and page categories."""

    def dispatch(self, request: t.Any, *args, **kwargs) -> t.Any:
        """Conform URL path location to the filesystem path."""
        self.location = Path(kwargs.get("location", ""))

        # URL location on the filesystem
        self.full_location = settings.PAGES_PATH / self.location

        # Possible places to find page content information
        self.category_path = self.full_location
        self.page_path = self.full_location.with_suffix(".md")

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self) -> t.List[str]:
        """Checks if the view uses the page template or listing template."""
        if self.page_path.is_file():
            template_name = "content/page.html"
        elif self.category_path.is_dir():
            template_name = "content/listing.html"
        else:
            raise Http404

        return [template_name]

    def get_context_data(self, **kwargs) -> t.Dict[str, t.Any]:
        """Assign proper context variables based on what resource user requests."""
        context = super().get_context_data(**kwargs)

        if self.page_path.is_file():
            context.update(self._get_page_context(self.page_path))
        elif self.category_path.is_dir():
            context.update(self._get_category_context(self.category_path))
            context["path"] = f"{self.location}/"  # Add trailing slash to simplify template
        else:
            raise Http404

        # Add subarticle information for dropdown menu if the page is also a category
        if self.page_path.is_file() and self.category_path.is_dir():
            context["subarticles"] = [
                path.stem for path in self.category_path.iterdir()
                if path.suffix != ".yml"
            ]

        context["breadcrumb_items"] = [
            {
                "name": utils.get_category(settings.PAGES_PATH / location)["title"],
                "path": str(location)
            } for location in reversed(self.location.parents)
        ]

        return context

    @staticmethod
    def _get_page_context(path: Path) -> t.Dict[str, t.Any]:
        page, metadata = utils.get_page(path)
        return {
            "page": page,
            "page_title": metadata["title"],
            "page_description": metadata["description"],
            "relevant_links": metadata.get("relevant_links", {}),
            "toc": metadata.get("toc")
        }

    @staticmethod
    def _get_category_context(path: Path) -> t.Dict[str, t.Any]:
        category = utils.get_category(path)
        return {
            "categories": utils.get_categories(path),
            "pages": utils.get_category_pages(path),
            "page_title": category["title"],
            "page_description": category["description"],
            "icon": category.get("icon"),
        }
