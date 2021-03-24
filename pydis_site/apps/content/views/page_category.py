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
        self.location = Path(self.kwargs.get("location", ""))
        self.full_location = settings.PAGES_PATH / self.location

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self) -> t.List[str]:
        """Checks if the view uses the page template or listing template."""
        if self.full_location.is_dir():
            template_name = "content/listing.html"
        elif self.full_location.with_suffix(".md").is_file():
            template_name = "content/page.html"
        else:
            raise Http404

        return [template_name]

    def get_context_data(self, **kwargs) -> t.Dict[str, t.Any]:
        """Assign proper context variables based on what resource user requests."""
        context = super().get_context_data(**kwargs)

        if self.full_location.is_dir():
            context["categories"] = utils.get_categories(self.full_location)
            category = utils.get_category(self.full_location)
            context["category_info"] = category
            context["page_title"] = category["name"]
            context["page_description"] = category["description"]
            context["pages"] = utils.get_category_pages(self.full_location)
            context["path"] = f"{self.location}/"  # Add trailing slash here to simplify template
        elif self.full_location.with_suffix(".md").is_file():
            page_result = utils.get_page(self.full_location.with_suffix(".md"))
            context["page"] = page_result
            context["page_title"] = page_result["metadata"]["title"]
            context["page_description"] = page_result["metadata"]["description"]
            context["relevant_links"] = page_result["metadata"].get("relevant_links", {})
        else:
            raise Http404

        breadcrumb_items = [
            {
                "name": utils.get_category(settings.PAGES_PATH / location)["name"],
                "path": str(location)
            } for location in self.location.parents
        ]
        context["breadcrumb_items"] = reversed(breadcrumb_items)

        return context
