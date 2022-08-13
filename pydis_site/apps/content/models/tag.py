from django.db import models


class Tag(models.Model):
    """A tag from the python-discord server."""

    last_updated = models.DateTimeField(
        help_text="The date and time this data was last fetched.",
        auto_now=True,
    )
    name = models.CharField(
        help_text="The tag's name.",
        primary_key=True,
        max_length=50,
    )
    body = models.TextField(help_text="The content of the tag.")
    url = models.URLField(help_text="The URL to this tag on GitHub.")
