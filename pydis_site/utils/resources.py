from __future__ import annotations

import yaml
import typing
import glob
from dataclasses import dataclass


@dataclass
class URL:
    icon: str
    title: str
    url: str


class Resource:
    description: str
    name: str
    payment: str
    payment_description: typing.Optional[str]
    urls: typing.List[URL]

    def __repr__(self):
        return f"<Resource name={self.name}>"

    @classmethod
    def construct_from_yaml(cls, yaml_data: str) -> Resource:  # noqa
        resource = cls()

        loaded = yaml.safe_load(yaml_data)

        resource.__dict__.update(loaded)

        resource.__dict__["urls"] = []

        for url in loaded["urls"]:
            resource.__dict__["urls"].append(URL(**url))

        return resource


class Category:
    resources: typing.List[Resource]
    name: str
    description: str

    def __repr__(self):
        return f"<Category name={self.name}>"

    @classmethod
    def construct_from_directory(cls, directory: str) -> Category:  # noqa
        category = cls()

        with open(f"{directory}/category_info.yaml") as category_info:
            category_data = yaml.safe_load(category_info)

            category.__dict__.update(category_data)

        category.resources = []

        for resource in glob.glob(f"{directory}/*.yaml"):
            if resource == f"{directory}/category_info.yaml":
                continue

            with open(resource) as res_file:
                category.resources.append(
                    Resource.construct_from_yaml(res_file)
                )

        return category


def load_categories(order: typing.List[str]) -> typing.List[Category]:
    categories = []
    for cat in order:
        direc = "pydis_site/apps/home/resources/" + cat
        categories.append(Category.construct_from_directory(direc))

    return categories
