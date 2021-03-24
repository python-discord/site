from pathlib import Path
from typing import Dict, Union

import yaml
from django.http import Http404
from markdown2 import markdown


def get_category(path: Path) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    if not path.exists() or not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text())


def get_categories(path: Path) -> Dict[str, Dict]:
    """Get information for all categories."""
    categories = {}

    for name in path.iterdir():
        if name.is_dir():
            categories[name.name] = get_category(path.joinpath(name.name))

    return categories


def get_pages(path: Path) -> Dict[str, Dict]:
    """Get all root or category page names and their metadata."""
    pages = {}

    for item in path.iterdir():
        if item.is_file() and item.name.endswith(".md"):
            md = markdown(item.read_text(), extras=["metadata"])
            pages[item.stem] = md.metadata

    return pages


def get_page(path: Path) -> Dict[str, Union[str, Dict]]:
    """Get one specific page."""
    if not path.exists() or not path.is_file():
        raise Http404("Page not found.")

    html = markdown(
        path.read_text(),
        extras=[
            "metadata",
            "fenced-code-blocks",
            "highlightjs-lang",
            "header-ids",
            "strike",
            "target-blank-links",
            "tables",
            "task_list"
        ]
    )

    return {"page": str(html), "metadata": html.metadata}
