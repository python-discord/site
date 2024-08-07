from pathlib import Path

import yaml
from django.apps import AppConfig

from pydis_site import settings
from pydis_site.apps.resources.templatetags.to_kebabcase import to_kebabcase

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


class ResourcesConfig(AppConfig):
    """AppConfig instance for Resources app."""

    name = 'pydis_site.apps.resources'

    @staticmethod
    def _sort_key_disregard_the(tuple_: tuple) -> str:
        """Sort a tuple by its key alphabetically, disregarding 'the' as a prefix."""
        name, resource = tuple_
        name = name.casefold()
        if name.startswith(("the ", "the_")):
            return name[4:]
        return name


    def ready(self) -> None:
        """Set up all the resources."""
        # Load the resources from the yaml files in /resources/
        self.resources = {
            path.stem: yaml.safe_load(path.read_text())
            for path in RESOURCES_PATH.rglob("*.yaml")
        }

        # Sort the resources alphabetically
        self.resources = dict(sorted(self.resources.items(), key=self._sort_key_disregard_the))

        # Parse out all current tags
        resource_tags = {
            "topics": set(),
            "payment_tiers": set(),
            "difficulty": set(),
            "type": set(),
        }
        for resource_name, resource in self.resources.items():
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

        # The bottom topic should always be "Other".
        self.filters["Topics"]["filters"].remove("Other")
        self.filters["Topics"]["filters"].append("Other")

        # A complete list of valid filter names
        self.valid_filters = {
            "topics": [to_kebabcase(topic) for topic in self.filters["Topics"]["filters"]],
            "payment-tiers": [
                to_kebabcase(tier) for tier in self.filters["Payment tiers"]["filters"]
            ],
            "type": [to_kebabcase(type_) for type_ in self.filters["Type"]["filters"]],
            "difficulty": [to_kebabcase(tier) for tier in self.filters["Difficulty"]["filters"]],
        }
