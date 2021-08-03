import typing as t
from collections import defaultdict
from functools import reduce
from itertools import chain
from operator import and_, or_
from pathlib import Path

import yaml
from django.conf import settings


def _transform_name(resource_name: str) -> str:
    return resource_name.title().replace('And', 'and', -1)


Resource = dict[str, t.Union[str, list[dict[str, str]], dict[str, list[str]]]]

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")

RESOURCES: dict[str, Resource] = {path.stem: yaml.safe_load(path.read_text()) for path
                                  in RESOURCES_PATH.rglob("*.yaml")}

RESOURCE_TABLE = {category: defaultdict(set) for category in (
    "topics",
    "payment_tiers",
    "complexity",
    "type"
)}

for name, resource in RESOURCES.items():
    for category, tags in resource['tags'].items():
        for tag in tags:
            RESOURCE_TABLE[category][_transform_name(tag)].add(name)


def yaml_file_matches_search(yaml_data: dict, search_terms: list[str]) -> bool:
    """Checks which resources contain tags for every search term passed."""
    search_terms = [x.lower() for x in search_terms]
    matching_tags = [x for x in chain(*yaml_data["tags"].values()) if x in search_terms]
    return len(matching_tags) >= len(search_terms)


def get_resources_from_search(search_categories: dict[str, set[str]]) -> list[Resource]:
    """Returns a list of all resources that match the given search terms."""
    resource_names_that_match = reduce(
        and_,
        (
            reduce(
                or_,
                (RESOURCE_TABLE[category][label] for label in labels),
                set()
            )
            for category, labels in search_categories.items()
        )
    )
    return [RESOURCES[name_] for name_ in resource_names_that_match]
