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


def get_resources_meta() -> dict:
    all_resources = get_resources()

    resource_meta_tags = {x: set() for x in default_categories}

    for resource in all_resources:
        tags = resource.get("tags")

        for tag_key, tag_values in tags.items():
            for tag_item in tag_values:
                resource_meta_tags[tag_key].add(tag_item)

    return resource_meta_tags


def get_resources() -> t.List[t.Dict]:
    """Loads resource YAMLs from provided path."""
    resources = []

    for item in RESOURCES_PATH.rglob("*.yaml"):
        resources.append(yaml.safe_load(item.read_text()))

    return resources
