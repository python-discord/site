import datetime
import functools
import tarfile
import tempfile
import typing
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
from .models import Tag

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

    This also includes some fake tags to preview the tag groups feature.
    This will return a cached value, so it should only be used for static builds.
    """
    tags = fetch_tags()
    for tag in tags[3:5]:  # pragma: no cover
        tag.group = "very-cool-group"
    return tags


def fetch_tags() -> list[Tag]:
    """
    Fetch tag data from the GitHub API.

    The entire repository is downloaded and extracted locally because
    getting file content would require one request per file, and can get rate-limited.
    """
    if settings.GITHUB_TOKEN:  # pragma: no cover
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
            group = None
            if tag_file.parent.name != "tags":
                # Tags in sub-folders are considered part of a group
                group = tag_file.parent.name

            tags.append(Tag(
                name=tag_file.name.removesuffix(".md"),
                group=group,
                body=tag_file.read_text(encoding="utf-8"),
            ))

    return tags


def get_tags() -> list[Tag]:
    """Return a list of all tags visible to the application, from the cache or API."""
    if settings.STATIC_BUILD:  # pragma: no cover
        last_update = None
    else:
        last_update = (
            Tag.objects.values_list("last_updated", flat=True)
            .order_by("last_updated").first()
        )

    if last_update is None or timezone.now() >= (last_update + TAG_CACHE_TTL):
        # Stale or empty cache
        if settings.STATIC_BUILD:  # pragma: no cover
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


def get_tag(path: str) -> typing.Union[Tag, list[Tag]]:
    """
    Return a tag based on the search location.

    The tag name and group must match. If only one argument is provided in the path,
    it's assumed to either be a group name, or a no-group tag name.

    If it's a group name, a list of tags which belong to it is returned.
    """
    path = path.split("/")
    if len(path) == 2:
        group, name = path[0], path[1]
    else:
        name = path[0]
        group = None

    matches = []
    for tag in get_tags():
        if tag.name == name and tag.group == group:
            return tag
        elif tag.group == name and group is None:
            matches.append(tag)

    if matches:
        return matches

    raise Tag.DoesNotExist()


def get_tag_category(
    tags: typing.Optional[list[Tag]] = None, *, collapse_groups: bool
) -> dict[str, dict]:
    """
    Generate context data for `tags`, or all tags if None.

    If `tags` is None, `get_tag` is used to populate the data.
    If `collapse_groups` is True, tags with parent groups are not included in the list,
    and instead the parent itself is included as a single entry with it's sub-tags
    in the description.
    """
    if not tags:
        tags = get_tags()

    data = []
    groups = {}

    # Create all the metadata for the tags
    for tag in tags:
        if tag.group is None or not collapse_groups:
            content = frontmatter.parse(tag.body)[1]
            data.append({
                "title": tag.name,
                "description": markdown.markdown(content, extensions=["pymdownx.superfences"]),
                "icon": "fas fa-tag",
            })
        else:
            if tag.group not in groups:
                groups[tag.group] = {
                    "title": tag.group,
                    "description": [tag.name],
                    "icon": "fas fa-tags",
                }
            else:
                groups[tag.group]["description"].append(tag.name)

    # Flatten group description into a single string
    for group in groups.values():
        # If the following string is updated, make sure to update it in the frontend JS as well
        group["description"] = "Contains the following tags: " + ", ".join(group["description"])
        data.append(group)

    # Sort the tags, and return them in the proper format
    return {tag["title"]: tag for tag in sorted(data, key=lambda tag: tag["title"].lower())}


def get_category_pages(path: Path) -> dict[str, dict]:
    """Get all page names and their metadata at a category path."""
    # Special handling for tags
    if path == Path(__file__).parent / "resources/tags":
        return get_tag_category(collapse_groups=True)

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
