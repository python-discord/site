from typing import Any, Dict

from django.views.generic import TemplateView

from pydis_site.apps.resources.utils import get_all_resources


class ResourcesListView(TemplateView):
    """Shows specific resources list."""

    template_name = "resources/resources_list.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Add resources and subcategories data into context."""
        context = super().get_context_data(**kwargs)
        context["resources"] = get_all_resources()

        return context
