import typing as t
from pathlib import Path

import yaml
from django.conf import settings

RESOURCES_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "resources", "resources")


def get_resources() -> t.List[t.Dict]:
    """Loads resource YAMLs from provided path."""
    resources = []

    for item in RESOURCES_PATH.rglob("*.yaml"):
        resources.append(yaml.safe_load(item.read_text()))

    return resources
