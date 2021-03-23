import os
from typing import Dict, List, Optional, Union

import yaml
from django.conf import settings
from django.http import Http404
from markdown2 import markdown


def get_category(path: List[str]) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    path = settings.ARTICLES_PATH.joinpath(*path)
    if not path.exists() or not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text())


def get_categories(path: Optional[List[str]] = None) -> Dict[str, Dict]:
    """Get all categories information."""
    categories = {}
    if path is None:
        categories_path = settings.ARTICLES_PATH
        path = []
    else:
        categories_path = settings.ARTICLES_PATH.joinpath(*path)

    for name in categories_path.iterdir():
        if name.is_dir():
            categories[name.name] = get_category([*path, name.name])

    return categories


def get_articles(path: Optional[List[str]] = None) -> Dict[str, Dict]:
    """Get all root or category articles."""
    if path is None:
        base_dir = settings.ARTICLES_PATH
    else:
        base_dir = settings.ARTICLES_PATH.joinpath(*path)

    articles = {}

    for item in base_dir.iterdir():
        if item.is_file() and item.name.endswith(".md"):
            md = markdown(item.read_text(), extras=["metadata"])
            articles[os.path.splitext(item.name)[0]] = md.metadata

    return articles


def get_article(path: List[str]) -> Dict[str, Union[str, Dict]]:
    """Get one specific article. When category is specified, get it from there."""
    article_path = settings.ARTICLES_PATH.joinpath(*path[:-1])

    # We need to include extension MD
    article_path = article_path.joinpath(f"{path[-1]}.md")
    if not article_path.exists() or not article_path.is_file():
        raise Http404("Article not found.")

    html = markdown(
        article_path.read_text(),
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

    return {"article": str(html), "metadata": html.metadata}
