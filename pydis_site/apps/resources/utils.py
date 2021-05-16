import typing as t
from pathlib import Path

import yaml


def get_resources(path: Path) -> t.List[t.Dict]:
    """Loads resource YAMLs from provided path."""
    resources = []

    for item in path.iterdir():
        if item.is_file() and item.suffix == ".yaml" and item.name != "_category_info.yaml":
            resources.append(yaml.safe_load(item.read_text()))

    return resources


def get_subcategories(path: Path) -> t.List[t.Dict]:
    """Loads resources subcategories with their resources by provided path."""
    subcategories = []

    for item in path.iterdir():
        if item.is_dir() and item.joinpath("_category_info.yaml").exists():
            subcategories.append({
                "category_info": {
                    **yaml.safe_load(
                        item.joinpath("_category_info.yaml").read_text()
                    ),
                    "raw_name": item.name
                },
                "resources": [
                    yaml.safe_load(subitem.read_text())
                    for subitem in item.iterdir()
                    if (
                        subitem.is_file()
                        and subitem.suffix == ".yaml"
                        and subitem.name != "_category_info.yaml"
                    )
                ]
            })

    return subcategories
