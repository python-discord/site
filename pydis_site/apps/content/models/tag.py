import collections.abc
import json

from django.db import models


class Commit(models.Model):
    """A git commit."""

    URL_BASE = "https://github.com/python-discord/bot/commit/"

    sha = models.CharField(
        help_text="The SHA hash of this commit.",
        primary_key=True,
        max_length=40,
    )
    message = models.TextField(help_text="The commit message.")
    date = models.DateTimeField(help_text="The date and time the commit was created.")
    author = models.TextField(help_text="The person(s) who created the commit.")

    @property
    def url(self) -> str:
        """The URL to the commit on GitHub."""
        return self.URL_BASE + self.sha

    def format_users(self) -> collections.abc.Iterable[str]:
        """Return a nice representation of the user(s)' name and email."""
        for author in json.loads(self.author):
            yield f"{author['name']} <{author['email']}>"


class Tag(models.Model):
    """A tag from the python-discord server."""

    URL_BASE = "https://github.com/python-discord/bot/tree/main/bot/resources/tags"

    last_updated = models.DateTimeField(
        help_text="The date and time this data was last fetched.",
        auto_now=True,
    )
    sha = models.CharField(
        help_text="The tag's hash, as calculated by GitHub.",
        max_length=40,
    )
    last_commit = models.ForeignKey(
        Commit,
        help_text="The commit this file was last touched in.",
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        help_text="The tag's name.",
        primary_key=True,
        max_length=50,
    )
    group = models.CharField(
        help_text="The group the tag belongs to.",
        null=True,
        max_length=50,
    )
    body = models.TextField(help_text="The content of the tag.")

    @property
    def url(self) -> str:
        """Get the URL of the tag on GitHub."""
        url = Tag.URL_BASE
        if self.group:
            url += f"/{self.group}"
        url += f"/{self.name}.md"
        return url
