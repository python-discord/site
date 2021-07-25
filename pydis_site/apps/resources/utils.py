import typing as t
from pathlib import Path

import yaml
from django.conf import settings

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


default_categories = [
    "topics",
    "payment_tiers",
    "complexity",
    "type"
]


def get_resources() -> list[dict[str, t.Union[list[str], str]]]:
    """Loads resource YAMLs from provided path."""
    return [yaml.safe_load(item.read_text()) for item in RESOURCES_PATH.rglob("*.yaml")]


def get_resources_meta() -> dict[str, list[str]]:
    """Combines the tags from each resource into one dictionary of unique tags."""
    resource_meta_tags = {x: set() for x in default_categories}

    for resource in get_resources():
        for tag_key, tag_values in resource.get("tags").items():
            for tag_item in tag_values:
                resource_meta_tags[tag_key].add(tag_item.title().replace('And', 'and', -1))

    return {key: sorted(value) for key, value in resource_meta_tags.items()}
