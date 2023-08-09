import collections.abc
import json

from django.db import models


class Commit(models.Model):
    """A git commit from the Python Discord Bot project."""

    URL_BASE = "https://github.com/python-discord/bot/commit/"

    sha = models.CharField(
        help_text="The SHA hash of this commit.",
        primary_key=True,
        max_length=40,
    )
    message = models.TextField(help_text="The commit message.")
    date = models.DateTimeField(help_text="The date and time the commit was created.")
    authors = models.TextField(help_text=(
        "The person(s) who created the commit. This is a serialized JSON object. "
        "Refer to the GitHub documentation on the commit endpoint "
        "(schema/commit.author & schema/commit.committer) for more info. "
        "https://docs.github.com/en/rest/commits/commits#get-a-commit"
    ))

    @property
    def url(self) -> str:
        """The URL to the commit on GitHub."""
        return self.URL_BASE + self.sha

    def lines(self) -> collections.abc.Iterable[str]:
        """Return each line in the commit message."""
        yield from self.message.split("\n")

    def format_authors(self) -> collections.abc.Iterable[str]:
        """Return a nice representation of the author(s)' name and email."""
        for author in json.loads(self.authors):
            yield f"{author['name']} <{author['email']}>"
