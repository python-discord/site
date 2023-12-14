from django.db import models

from .commit import Commit


class Tag(models.Model):
    """A tag from the python-discord bot repository."""

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
