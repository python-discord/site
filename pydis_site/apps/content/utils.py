import datetime
import functools
import json
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
from .models import Commit, Tag

TAG_CACHE_TTL = datetime.timedelta(hours=1)


def github_client(**kwargs) -> httpx.Client:
    """Get a client to access the GitHub API with important settings pre-configured."""
    client = httpx.Client(
        base_url=settings.GITHUB_API,
        follow_redirects=True,
        timeout=settings.TIMEOUT_PERIOD,
        **kwargs
    )
    if settings.GITHUB_TOKEN:  # pragma: no cover
        if not client.headers.get("Authorization"):
            client.headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}

    return client


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
    client = github_client()

    # Grab metadata
    metadata = client.get("/repos/python-discord/bot/contents/bot/resources")
    metadata.raise_for_status()

    hashes = {}
    for entry in metadata.json():
        if entry["type"] == "dir":
            # Tag group
            files = client.get(entry["url"])
            files.raise_for_status()
            files = files.json()
        else:
            files = [entry]

        for file in files:
            hashes[file["name"]] = file["sha"]

    # Download the files
    tar_file = client.get("/repos/python-discord/bot/tarball")
    tar_file.raise_for_status()

    client.close()

    tags = []
    with tempfile.TemporaryDirectory() as folder:
        with tarfile.open(fileobj=BytesIO(tar_file.content)) as repo:
            included = []
            for file in repo.getmembers():
                if "/bot/resources/tags" in file.path:
                    included.append(file)
            repo.extractall(folder, included)

        for tag_file in Path(folder).rglob("*.md"):
            name = tag_file.name
            group = None
            if tag_file.parent.name != "tags":
                # Tags in sub-folders are considered part of a group
                group = tag_file.parent.name

            tags.append(Tag(
                name=name.removesuffix(".md"),
                sha=hashes[name],
                group=group,
                body=tag_file.read_text(encoding="utf-8"),
                last_commit=None,
            ))

    return tags


def set_tag_commit(tag: Tag) -> None:
    """Fetch commit information from the API, and save it for the tag."""
    if settings.STATIC_BUILD:  # pragma: no cover
        # Static builds request every page during build, which can ratelimit it.
        # Instead, we return some fake data.
        tag.last_commit = Commit(
            sha="68da80efc00d9932a209d5cccd8d344cec0f09ea",
            message="Initial Commit\n\nTHIS IS FAKE DEMO DATA",
            date=datetime.datetime(2018, 2, 3, 12, 20, 26, tzinfo=datetime.timezone.utc),
            author=json.dumps([{"name": "Joseph", "email": "joseph@josephbanks.me"}]),
        )
        return

    path = "/bot/resources/tags"
    if tag.group:
        path += f"/{tag.group}"
    path += f"/{tag.name}.md"

    # Fetch and set the commit
    with github_client() as client:
        data = client.get("/repos/python-discord/bot/commits", params={"path": path})
        data.raise_for_status()
        data = data.json()[0]

    commit = data["commit"]
    author, committer = commit["author"], commit["committer"]

    date = datetime.datetime.strptime(committer["date"], settings.GITHUB_TIMESTAMP_FORMAT)
    date = date.replace(tzinfo=datetime.timezone.utc)

    if author["email"] == committer["email"]:
        commit_author = [author]
    else:
        commit_author = [author, committer]

    commit_obj, _ = Commit.objects.get_or_create(
        sha=data["sha"],
        message=commit["message"],
        date=date,
        author=json.dumps(commit_author),
    )
    tag.last_commit = commit_obj
    tag.save()


def record_tags(tags: list[Tag]) -> None:
    """Sync the database with an updated set of tags."""
    # Remove entries which no longer exist
    Tag.objects.exclude(name__in=[tag.name for tag in tags]).delete()

    # Insert/update the tags
    for tag in tags:
        try:
            old_tag = Tag.objects.get(name=tag.name)
        except Tag.DoesNotExist:
            # The tag is not in the database yet,
            # pretend it's previous state is the current state
            old_tag = tag

        if old_tag.sha == tag.sha and old_tag.last_commit is not None:
            # We still have an up-to-date commit entry
            tag.last_commit = old_tag.last_commit

        tag.save()

    # Drop old, unused commits
    Commit.objects.filter(tag__isnull=True).delete()


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
            record_tags(tags)

        return tags
    else:
        # Get tags from database
        return Tag.objects.all()


def get_tag(path: str, *, skip_sync: bool = False) -> typing.Union[Tag, list[Tag]]:
    """
    Return a tag based on the search location.

    If certain tag data is out of sync (for instance a commit date is missing),
    an extra request will be made to sync the information.

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
            if tag.last_commit is None and not skip_sync:
                set_tag_commit(tag)
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
