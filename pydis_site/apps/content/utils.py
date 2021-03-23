import os
from typing import Dict, List, Optional, Union

import yaml
from django.conf import settings
from django.http import Http404
from markdown2 import markdown


def get_category(path: List[str]) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    path = settings.PAGES_PATH.joinpath(*path)
    if not path.exists() or not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text())


def get_categories(path: Optional[List[str]] = None) -> Dict[str, Dict]:
    """Get all categories information."""
    categories = {}
    if path is None:
        categories_path = settings.PAGES_PATH
        path = []
    else:
        categories_path = settings.PAGES_PATH.joinpath(*path)

    for name in categories_path.iterdir():
        if name.is_dir():
            categories[name.name] = get_category([*path, name.name])

    return categories


def get_pages(path: Optional[List[str]] = None) -> Dict[str, Dict]:
    """Get all root or category pages."""
    if path is None:
        base_dir = settings.PAGES_PATH
    else:
        base_dir = settings.PAGES_PATH.joinpath(*path)

    pages = {}

    for item in base_dir.iterdir():
        if item.is_file() and item.name.endswith(".md"):
            md = markdown(item.read_text(), extras=["metadata"])
            pages[os.path.splitext(item.name)[0]] = md.metadata

    return pages


def get_page(path: List[str]) -> Dict[str, Union[str, Dict]]:
    """Get one specific page. When category is specified, get it from there."""
    page_path = settings.PAGES_PATH.joinpath(*path[:-1])

    # We need to include extension MD
    page_path = page_path.joinpath(f"{path[-1]}.md")
    if not page_path.exists() or not page_path.is_file():
        raise Http404("Page not found.")

    html = markdown(
        page_path.read_text(),
        extras=[
            "metadata",
            "fenced-code-blocks",
            "header-ids",
            "strike",
            "target-blank-links",
            "tables",
            "task_list"
        ]
    )

    return {"page": str(html), "metadata": html.metadata}
