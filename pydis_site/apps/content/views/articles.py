from django.views.generic import TemplateView

from pydis_site.apps.content.utils import get_articles, get_categories


class ArticlesView(TemplateView):
    """Shows all content and categories."""

    template_name = "content/listing.html"

    def get_context_data(self, **kwargs) -> dict:
        """Add articles and categories data to template context."""
        context = super().get_context_data(**kwargs)
        context["content"] = get_articles()
        context["categories"] = get_categories()
        return context
