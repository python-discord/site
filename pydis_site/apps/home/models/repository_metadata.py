from django.db import models


class RepositoryMetadata(models.Model):
    """Information about one of our repos fetched from the GitHub API."""

    last_updated = models.DateTimeField(
        help_text="The date and time this data was last fetched.",
        auto_now=True,
    )
    repo_name = models.CharField(
        primary_key=True,
        max_length=40,
        help_text="The full name of the repo, e.g. python-discord/site",
    )
    description = models.CharField(
        max_length=400,
        help_text="The description of the repo.",
    )
    forks = models.IntegerField(
        help_text="The number of forks of this repo",
    )
    stargazers = models.IntegerField(
        help_text="The number of stargazers for this repo",
    )
    language = models.CharField(
        max_length=20,
        help_text="The primary programming language used for this repo.",
    )

    def __str__(self):
        """Returns the repo name, for display purposes."""
        return self.repo_name
