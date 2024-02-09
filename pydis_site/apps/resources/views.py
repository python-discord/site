import json
from pathlib import Path

import yaml
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View

from pydis_site import settings
from pydis_site.apps.resources.templatetags.to_kebabcase import to_kebabcase

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


def sort_key_disregard_the(tuple_: tuple) -> str:
    """Sort a tuple by its key alphabetically, disregarding 'the' as a prefix."""
    name, resource = tuple_
    name = name.casefold()
    if name.startswith(("the ", "the_")):
        return name[4:]
    return name


def load_resources() -> tuple[dict, dict, dict]:
    """Return resources, filters, and valid filters as parsed from the resources data directory."""
    # Load the resources from the yaml files in /resources/
    resources = {
        path.stem: yaml.safe_load(path.read_text())
        for path in RESOURCES_PATH.rglob("*.yaml")
    }

    # Sort the resources alphabetically
    resources = dict(sorted(resources.items(), key=sort_key_disregard_the))

    # Parse out all current tags
    resource_tags = {
        "topics": set(),
        "payment_tiers": set(),
        "difficulty": set(),
        "type": set(),
    }
    for resource_name, resource in resources.items():
        css_classes = []
        for tag_type in resource_tags:
            # Store the tags into `resource_tags`
            tags = resource.get("tags", {}).get(tag_type, [])
            for tag in tags:
                tag = tag.title()
                tag = tag.replace("And", "and")
                resource_tags[tag_type].add(tag)

            # Make a CSS class friendly representation too, while we're already iterating.
            for tag in tags:
                css_tag = to_kebabcase(f"{tag_type}-{tag}")
                css_classes.append(css_tag)

        # Now add the css classes back to the resource, so we can use them in the template.
        resources[resource_name]["css_classes"] = " ".join(css_classes)

    # Set up all the filter checkbox metadata
    filters = {
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

    # The bottom topic should always be "Other".
    filters["Topics"]["filters"].remove("Other")
    filters["Topics"]["filters"].append("Other")

    # A complete list of valid filter names
    valid_filters = {
        "topics": [to_kebabcase(topic) for topic in filters["Topics"]["filters"]],
        "payment_tiers": [
            to_kebabcase(tier) for tier in filters["Payment tiers"]["filters"]
        ],
        "type": [to_kebabcase(type_) for type_ in filters["Type"]["filters"]],
        "difficulty": [to_kebabcase(tier) for tier in filters["Difficulty"]["filters"]],
    }

    return (resources, filters, valid_filters)


class ResourceView(View):
    """Our curated list of good learning resources."""

    def __init__(self, *args, **kwargs):
        """Set up all the resources."""
        super().__init__(*args, **kwargs)
        self.resources, self.filters, self.valid_filters = load_resources()

    def get(self, request: WSGIRequest, resource_type: str | None = None) -> HttpResponse:
        """List out all the resources, and any filtering options from the URL."""
        # Add type filtering if the request is made to somewhere like /resources/video.
        # We also convert all spaces to dashes, so they'll correspond with the filters.
        if resource_type:
            dashless_resource_type = resource_type.replace("-", " ")

            if dashless_resource_type.title() not in self.filters["Type"]["filters"]:
                return HttpResponseNotFound()

            resource_type = resource_type.replace(" ", "-")

        return render(
            request,
            template_name="resources/resources.html",
            context={
                "resources": self.resources,
                "filters": self.filters,
                "valid_filters": json.dumps(self.valid_filters),
                "resource_type": resource_type,
            }
        )


class ResourceFilterView(View):
    """Exposes resource filters for the bot."""

    def __init__(self, *args, **kwargs):
        """Load resource filters."""
        super().__init__(*args, **kwargs)
        _, self.filters, self.valid_filters = load_resources()

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Return resource filters as JSON."""
        return JsonResponse(
            {
                'filters': self.filters,
                'valid_filters': self.valid_filters
            }
        )
