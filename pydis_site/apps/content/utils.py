from pathlib import Path
from typing import Dict, Union

import yaml
from django.http import Http404
from markdown2 import markdown


def get_category(path: Path) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    if not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text(encoding="utf-8"))


def get_categories(path: Path) -> Dict[str, Dict]:
    """Get information for all categories."""
    categories = {}

    for item in path.iterdir():
        if item.is_dir():
            categories[item.name] = get_category(item)

    return categories


def get_category_pages(path: Path) -> Dict[str, Dict]:
    """Get all page names and their metadata at a category path."""
    pages = {}

    for item in path.glob("*.md"):
        if item.is_file():
            md = markdown(item.read_text(), extras=["metadata"])
            pages[item.stem] = md.metadata

    return pages


def get_page(path: Path) -> Dict[str, Union[str, Dict]]:
    """Get one specific page."""
    if not path.is_file():
        raise Http404("Page not found.")

    html = markdown(
        path.read_text(encoding="utf-8"),
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

    return {"content": str(html), "metadata": html.metadata}
