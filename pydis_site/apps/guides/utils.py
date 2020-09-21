import os
from typing import Dict, Optional, Union

import yaml
from django.conf import settings
from django.http import Http404
from markdown import Markdown


def _get_base_path() -> str:
    """Have extra function for base path getting for testability."""
    return os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides")


def get_category(category: str) -> Dict[str, str]:
    """Load category information by name from _info.yml."""
    path = os.path.join(_get_base_path(), category)
    if not os.path.exists(path) or not os.path.isdir(path):
        raise Http404("Category not found.")

    with open(os.path.join(path, "_info.yml")) as f:
        return yaml.load(f.read())


def get_categories() -> Dict[str, Dict]:
    """Get all categories information."""
    base_path = _get_base_path()
    categories = {}

    for name in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, name)):
            categories[name] = get_category(name)

    return categories


def get_guides(category: Optional[str] = None) -> Dict[str, Dict]:
    """Get all root guides when category is not specified. Otherwise get all this category guides."""
    if category is None:
        base_dir = _get_base_path()
    else:
        base_dir = os.path.join(_get_base_path(), category)

    guides = {}

    for filename in os.listdir(base_dir):
        full_path = os.path.join(base_dir, filename)
        if os.path.isfile(full_path) and filename.endswith(".md"):
            md = Markdown(extensions=['meta'])
            with open(full_path) as f:
                md.convert(f.read())

            guides[os.path.splitext(filename)[0]] = md.Meta

    return guides


def get_guide(guide: str, category: Optional[str]) -> Dict[str, Union[str, Dict]]:
    """Get one specific guide. When category is specified, get it from there."""
    if category is None:
        base_path = _get_base_path()
    else:
        base_path = os.path.join(_get_base_path(), category)

        if not os.path.exists(base_path) or not os.path.isdir(base_path):
            raise Http404("Category not found.")

    guide_path = os.path.join(base_path, f"{guide}.md")
    if not os.path.exists(guide_path) or not os.path.isfile(guide_path):
        raise Http404("Guide not found.")

    md = Markdown(extensions=['meta', 'attr_list', 'fenced_code'])

    with open(guide_path) as f:
        html = md.convert(f.read())

    return {"guide": html, "metadata": md.Meta}
