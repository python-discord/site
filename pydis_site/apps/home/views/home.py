import logging
from typing import Dict, List

import requests
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from pydis_site.apps.home.models import RepositoryMetadata

log = logging.getLogger(__name__)


class HomeView(View):
    """The main landing page for the website."""

    github_api = "https://api.github.com/users/python-discord/repos?per_page=100"
    repository_cache_ttl = 3600

    # Which of our GitHub repos should be displayed on the front page, and in which order?
    repos = [
        "python-discord/site",
        "python-discord/bot",
        "python-discord/snekbox",
        "python-discord/sir-lancebot",
        "python-discord/metricity",
        "python-discord/django-simple-bulma",
    ]

    def __init__(self):
        """Clean up stale RepositoryMetadata."""
        RepositoryMetadata.objects.exclude(repo_name__in=self.repos).delete()

    def _get_api_data(self) -> Dict[str, Dict[str, str]]:
        """
        Call the GitHub API and get information about our repos.

        If we're unable to get that info for any reason, return an empty dict.
        """
        repo_dict = {}

        # Fetch the data from the GitHub API
        api_data: List[dict] = requests.get(self.github_api).json()

        # Process the API data into our dict
        for repo in api_data:
            try:
                full_name = repo["full_name"]

                if full_name in self.repos:
                    repo_dict[full_name] = {
                        "full_name": repo["full_name"],
                        "description": repo["description"],
                        "language": repo["language"],
                        "forks_count": repo["forks_count"],
                        "stargazers_count": repo["stargazers_count"],
                    }
            # Something is not right about the API data we got back from GitHub.
            except (TypeError, ConnectionError, KeyError) as e:
                log.error(
                    "Unable to parse the GitHub repository metadata from response!",
                    extra={
                        'api_data': api_data,
                        'error': e
                    }
                )
                continue

        return repo_dict

    def _get_repo_data(self) -> List[RepositoryMetadata]:
        """Build a list of RepositoryMetadata objects that we can use to populate the front page."""
        database_repositories = []

        # First, let's see if we have any metadata cached.
        cached_data = RepositoryMetadata.objects.all()

        # If we don't, we have to create some!
        if not cached_data:

            # Try to get new data from the API. If it fails, we'll return an empty list.
            # In this case, we simply don't display our projects on the site.
            api_repositories = self._get_api_data()

            # Create all the repodata records in the database.
            for api_data in api_repositories.values():
                repo_data = RepositoryMetadata(
                    repo_name=api_data["full_name"],
                    description=api_data["description"],
                    forks=api_data["forks_count"],
                    stargazers=api_data["stargazers_count"],
                    language=api_data["language"],
                )

                repo_data.save()
                database_repositories.append(repo_data)

            return database_repositories

        # If the data is stale, we should refresh it.
        if (timezone.now() - cached_data[0].last_updated).seconds > self.repository_cache_ttl:
            # Try to get new data from the API. If it fails, return the cached data.
            api_repositories = self._get_api_data()

            if not api_repositories:
                return RepositoryMetadata.objects.all()

            # Update or create all RepoData objects in self.repos
            for repo_name, api_data in api_repositories.items():
                try:
                    repo_data = RepositoryMetadata.objects.get(repo_name=repo_name)
                    repo_data.description = api_data["description"]
                    repo_data.language = api_data["language"]
                    repo_data.forks = api_data["forks_count"]
                    repo_data.stargazers = api_data["stargazers_count"]
                except RepositoryMetadata.DoesNotExist:
                    repo_data = RepositoryMetadata(
                        repo_name=api_data["full_name"],
                        description=api_data["description"],
                        forks=api_data["forks_count"],
                        stargazers=api_data["stargazers_count"],
                        language=api_data["language"],
                    )
                repo_data.save()
                database_repositories.append(repo_data)
            return database_repositories

        # Otherwise, if the data is fresher than 2 minutes old, we should just return it.
        else:
            return RepositoryMetadata.objects.all()

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Collect repo data and render the homepage view."""
        repo_data = self._get_repo_data()
        return render(request, "home/index.html", {"repo_data": repo_data})


def timeline(request: WSGIRequest) -> HttpResponse:
    """Render timeline view."""
    return render(request, 'home/timeline.html')
