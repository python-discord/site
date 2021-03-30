from pathlib import Path
from typing import Any, Dict

import yaml
from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

from pydis_site.apps.resources.utils import get_resources, get_subcategories

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


class ResourcesListView(TemplateView):
    """Shows specific resources list."""

    template_name = "resources/resources_list.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Add resources and subcategories data into context."""
        context = super().get_context_data(**kwargs)

        resource_path = RESOURCES_PATH / self.kwargs["type"]
        if (
                not resource_path.is_dir()
                or not resource_path.joinpath("_category_info.yaml").exists()
        ):
            raise Http404

        context["resources"] = get_resources(resource_path)
        context["subcategories"] = get_subcategories(resource_path)
        context["category_info"] = {
            **yaml.safe_load(
                resource_path.joinpath("_category_info.yaml").read_text()
            ),
            "raw_name": resource_path.name
        }

        return context
