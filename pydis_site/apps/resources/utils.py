import typing as t
from itertools import chain
from pathlib import Path

import yaml
from django.conf import settings

Resource = dict[str, t.Union[str, list[dict[str, str]], dict[str, list[str]]]]

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")

default_categories = [
    "topics",
    "payment_tiers",
    "complexity",
    "type"
]


def yaml_file_matches_search(yaml_data: dict, search_terms: list[str]) -> bool:
    """Checks which resources contain tags for every search term passed."""
    search_terms = [x.lower() for x in search_terms]
    matching_tags = [x for x in chain(*yaml_data["tags"].values()) if x in search_terms]
    return len(matching_tags) >= len(search_terms)


def get_resources_from_search(search_categories: list[str]) -> list[Resource]:
    """Returns a list of all resources that match the given search terms."""
    out = []
    for item in RESOURCES_PATH.rglob("*.yaml"):
        this_dict = yaml.safe_load(item.read_text())
        if yaml_file_matches_search(this_dict, search_categories):
            out.append(this_dict)
    return out


def get_all_resources() -> list[dict[str, t.Union[list[str], str]]]:
    """Loads resource YAMLs from provided path."""
    return [yaml.safe_load(item.read_text()) for item in RESOURCES_PATH.rglob("*.yaml")]


def get_resources_meta() -> dict[str, list[str]]:
    """Combines the tags from each resource into one dictionary of unique tags."""
    resource_meta_tags = {x: set() for x in default_categories}

    for resource in get_all_resources():
        for tag_key, tag_values in resource.get("tags").items():
            for tag_item in tag_values:
                resource_meta_tags[tag_key].add(tag_item.title().replace('And', 'and', -1))

    return {key: sorted(value) for key, value in resource_meta_tags.items()}
