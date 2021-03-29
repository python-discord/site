from pathlib import Path
from typing import Dict, Tuple

import frontmatter
import markdown
import yaml
from django.http import Http404
from markdown.extensions.toc import TocExtension


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
            pages[item.stem] = frontmatter.load(item).metadata

    return pages


def get_page(path: Path) -> Tuple[str, Dict]:
    """Get one specific page."""
    if not path.is_file():
        raise Http404("Page not found.")

    metadata, content = frontmatter.parse(path.read_text(encoding="utf-8"))
    toc_depth = metadata.get("toc", 1)

    md = markdown.Markdown(
        extensions=[
            "extra",
            # Empty string for marker to disable text searching for [TOC]
            # By using a metadata key instead, we save time on long markdown documents
            TocExtension(permalink=True, marker="", toc_depth=toc_depth)
        ]
    )
    html = md.convert(content)

    # Don't set the TOC if the metadata does not specify one
    if "toc" in metadata:
        metadata["toc"] = md.toc

    return str(html), metadata
