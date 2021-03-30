from pathlib import Path
from typing import Any, Dict

import yaml
from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


class ResourcesListView(TemplateView):
    """Shows specific resources list."""

    template_name = "resources/resources_list.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Add resources and subcategories data into context."""
        context = super().get_context_data(**kwargs)

        resource_path = RESOURCES_PATH / self.kwargs["type"]
        if (
                not resource_path.exists()
                or not resource_path.is_dir()
                or not resource_path.joinpath("_category_info.yaml").exists()
        ):
            raise Http404

        resources = []
        subcategories = []
        for item in resource_path.iterdir():
            if item.is_file() and item.suffix == ".yaml" and item.name != "_category_info.yaml":
                resources.append(yaml.safe_load(item.read_text()))
            elif item.is_dir() and item.joinpath("_category_info.yaml").exists():
                subcategories.append({
                    "category_info": {**yaml.safe_load(
                        item.joinpath("_category_info.yaml").read_text()
                    ), "raw_name": item.name},
                    "resources": sorted([
                        yaml.safe_load(subitem.read_text())
                        for subitem in item.iterdir()
                        if (
                            subitem.is_file()
                            and subitem.suffix == ".yaml"
                            and subitem.name != "_category_info.yaml"
                        )
                    ], key=lambda k: k.get('position', 100))
                })

        context["resources"] = sorted(resources, key=lambda k: k.get('position', 100))
        context["subcategories"] = sorted(
            subcategories, key=lambda k: k.get('category_info', {}).get('position', 100)
        )
        context["category_info"] = {**yaml.safe_load(
            resource_path.joinpath("_category_info.yaml").read_text()
        ), "raw_name": resource_path.name}

        return context
