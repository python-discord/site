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


def yaml_file_matches_search(yaml_data: dict[str, t.Union[list[str], str]], search_terms: list[str]) -> bool:
    match_count = 0
    search_len = len(search_terms)
    for search in search_terms:
        for _, values in yaml_data["tags"].items():
            if search.lower() in values:
                match_count += 1
                if match_count >= search_len:
                    return True
    return False


def get_resources_from_search(search_categories: list[str]) -> list[dict[str, t.Union[list[str], str]]]:
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
