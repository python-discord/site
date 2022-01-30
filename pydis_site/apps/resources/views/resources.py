from pathlib import Path
import typing as t

import yaml
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from pydis_site import settings

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


class ResourceView(View):
    """Our curated list of good learning resources."""

    def __init__(self, *args, **kwargs):
        """Set up all the resources."""
        super().__init__(*args, **kwargs)

        # Load the resources from the yaml files in /resources/
        self.resources = {
            path.stem: yaml.safe_load(path.read_text())
            for path in RESOURCES_PATH.rglob("*.yaml")
        }

        # Sort the resources alphabetically
        self.resources = dict(sorted(self.resources.items()))

        # Parse out all current tags
        resource_tags = {
            "topics": set(),
            "payment_tiers": set(),
            "difficulty": set(),
            "type": set(),
        }
        for resource_name, resource in self.resources.items():
            css_classes = []
            for tag_type in resource_tags.keys():
                # Store the tags into `resource_tags`
                tags = resource.get("tags", {}).get(tag_type, [])
                for tag in tags:
                    tag = tag.title()
                    tag = tag.replace("And", "and")
                    resource_tags[tag_type].add(tag)

                # Make a CSS class friendly representation too, while we're already iterating.
                for tag in tags:
                    css_tag = f"{tag_type}-{tag}"
                    css_tag = css_tag.replace("_", "-")
                    css_tag = css_tag.replace(" ", "-")
                    css_classes.append(css_tag)

            # Now add the css classes back to the resource, so we can use them in the template.
            self.resources[resource_name]["css_classes"] = " ".join(css_classes)

        # Set up all the filter checkbox metadata
        self.filters = {
            "Difficulty": {
                "filters": sorted(resource_tags.get("difficulty")),
                "icon": "fas fa-brain",
                "hidden": False,
            },
            "Type": {
                "filters": sorted(resource_tags.get("type")),
                "icon": "fas fa-photo-video",
                "hidden": False,
            },
            "Payment tiers": {
                "filters": sorted(resource_tags.get("payment_tiers")),
                "icon": "fas fa-dollar-sign",
                "hidden": True,
            },
            "Topics": {
                "filters": sorted(resource_tags.get("topics")),
                "icon": "fas fa-lightbulb",
                "hidden": True,
            }
        }

    def get(self, request: WSGIRequest, resource_type: t.Optional[str] = None) -> HttpResponse:
        """List out all the resources, and any filtering options from the URL."""

        # Add type filtering if the request is made to somewhere like /resources/video
        if resource_type and resource_type.title() not in self.filters['Type']['filters']:
            return HttpResponseNotFound()

        return render(
            request,
            template_name="resources/resources.html",
            context={
                "resources": self.resources,
                "filters": self.filters,
                "resource_type": resource_type,
            }
        )
