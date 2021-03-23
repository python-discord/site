from django.views.generic import TemplateView

from pydis_site.apps.content.utils import get_pages, get_categories


class PagesView(TemplateView):
    """Shows all pages and categories."""

    template_name = "content/listing.html"

    def get_context_data(self, **kwargs) -> dict:
        """Add page and category data to template context."""
        context = super().get_context_data(**kwargs)
        context["content"] = get_pages()
        context["categories"] = get_categories()
        return context
