import datetime
import functools
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

import frontmatter
import httpx
import markdown
import yaml
from django.http import Http404
from django.utils import timezone
from markdown.extensions.toc import TocExtension

from pydis_site import settings
from .models.tag import Tag

TAG_URL_BASE = "https://github.com/python-discord/bot/tree/main/bot/resources/tags"
TAG_CACHE_TTL = datetime.timedelta(hours=1)


def get_category(path: Path) -> dict[str, str]:
    """Load category information by name from _info.yml."""
    if not path.is_dir():
        raise Http404("Category not found.")

    return yaml.safe_load(path.joinpath("_info.yml").read_text(encoding="utf-8"))


def get_categories(path: Path) -> dict[str, dict]:
    """Get information for all categories."""
    categories = {}

    for item in path.iterdir():
        if item.is_dir():
            categories[item.name] = get_category(item)

    return categories


@functools.cache
def get_tags_static() -> list[Tag]:
    """
    Fetch tag information in static builds.

    This will return a cached value, so it should only be used for static builds.
    """
    return fetch_tags()


def fetch_tags() -> list[Tag]:
    """
    Fetch tag data from the GitHub API.

    The entire repository is downloaded and extracted locally because
    getting file content would require one request per file, and can get rate-limited.
    """
    if settings.GITHUB_TOKEN:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
    else:
        headers = {}

    tar_file = httpx.get(
        f"{settings.GITHUB_API}/repos/python-discord/bot/tarball",
        follow_redirects=True,
        timeout=settings.TIMEOUT_PERIOD,
        headers=headers,
    )
    tar_file.raise_for_status()

    tags = []
    with tempfile.TemporaryDirectory() as folder:
        with tarfile.open(fileobj=BytesIO(tar_file.content)) as repo:
            included = []
            for file in repo.getmembers():
                if "/bot/resources/tags" in file.path:
                    included.append(file)
            repo.extractall(folder, included)

        for tag_file in Path(folder).rglob("*.md"):
            tags.append(Tag(
                name=tag_file.name.removesuffix(".md"),
                body=tag_file.read_text(encoding="utf-8"),
                url=f"{TAG_URL_BASE}/{tag_file.name}"
            ))

    return tags


def get_tags() -> list[Tag]:
    """Return a list of all tags visible to the application, from the cache or API."""
    if settings.STATIC_BUILD:
        last_update = None
    else:
        last_update = (
            Tag.objects.values_list("last_updated", flat=True)
            .order_by("last_updated").first()
        )

    if last_update is None or timezone.now() >= (last_update + TAG_CACHE_TTL):
        # Stale or empty cache
        if settings.STATIC_BUILD:
            tags = get_tags_static()
        else:
            tags = fetch_tags()
            Tag.objects.exclude(name__in=[tag.name for tag in tags]).delete()
            for tag in tags:
                tag.save()

        return tags
    else:
        # Get tags from database
        return Tag.objects.all()


def get_tag(name: str) -> Tag:
    """Return a tag by name."""
    tags = get_tags()
    for tag in tags:
        if tag.name == name:
            return tag

    raise Tag.DoesNotExist()


def get_category_pages(path: Path) -> dict[str, dict]:
    """Get all page names and their metadata at a category path."""
    # Special handling for tags
    if path == Path(__file__).parent / "resources/tags":
        tags = {}
        for tag in get_tags():
            content = frontmatter.parse(tag.body)[1]
            if len(content) > 100:
                # Trim the preview to a maximum of 100 visible characters
                # This causes some markdown to break, but we ignore that
                content = content[:100] + "..."

            tags[tag.name] = {
                "title": tag.name,
                "description": markdown.markdown(content),
                "icon": "fas fa-tag"
            }

        return {name: tags[name] for name in sorted(tags)}

    pages = {}

    for item in path.glob("*.md"):
        # Only list page if there is no category with the same name
        if item.is_file() and not item.with_suffix("").is_dir():
            pages[item.stem] = frontmatter.load(item).metadata

    return pages


def get_page(path: Path) -> tuple[str, dict]:
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
