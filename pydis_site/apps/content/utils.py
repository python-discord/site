import os
from pathlib import Path
from typing import Dict, Optional, Union

import yaml
from django.conf import settings
from django.http import Http404
from markdown2 import markdown


def _get_base_path() -> Path:
    """Have extra function for base path getting for testability."""
    return Path(settings.BASE_DIR, "pydis_site", "apps", "content", "resources", "content")


def get_category(category: str) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    path = _get_base_path().joinpath(category)
    if not path.exists() or not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text())


def get_categories() -> Dict[str, Dict]:
    """Get all categories information."""
    base_path = _get_base_path()
    categories = {}

    for name in base_path.iterdir():
        if name.is_dir():
            categories[name.name] = get_category(name.name)

    return categories


def get_articles(category: Optional[str] = None) -> Dict[str, Dict]:
    """Get all root content when category is not specified. Otherwise get all this category content."""
    if category is None:
        base_dir = _get_base_path()
    else:
        base_dir = _get_base_path().joinpath(category)

    articles = {}

    for item in base_dir.iterdir():
        if item.is_file() and item.name.endswith(".md"):
            md = markdown(item.read_text(), extras=["metadata"])
            articles[os.path.splitext(item.name)[0]] = md.metadata

    return articles


def get_article(article: str, category: Optional[str]) -> Dict[str, Union[str, Dict]]:
    """Get one specific article. When category is specified, get it from there."""
    if category is None:
        base_path = _get_base_path()
    else:
        base_path = _get_base_path().joinpath(category)

        if not base_path.exists() or not base_path.is_dir():
            raise Http404("Category not found.")

    article_path = base_path.joinpath(f"{article}.md")
    if not article_path.exists() or not article_path.is_file():
        raise Http404("Article not found.")

    html = markdown(
        article_path.read_text(),
        extras=["metadata", "fenced-code-blocks", "header-ids", "strike", "target-blank-links", "tables", "task_list"]
    )

    return {"article": str(html), "metadata": html.metadata}
