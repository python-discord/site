import logging
from typing import Dict, List

import httpx
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from pydis_site import settings
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
        "python-discord/king-arthur",
    ]

    def __init__(self):
        """Clean up stale RepositoryMetadata."""
        if not settings.STATIC_BUILD:
            RepositoryMetadata.objects.exclude(repo_name__in=self.repos).delete()

        # If no token is defined (for example in local development), then
        # it does not make sense to pass the Authorization header. More
        # specifically, GitHub will reject any requests from us due to the
        # invalid header. We can make a limited number of anonymous requests
        # though, which is useful for testing.
        if settings.GITHUB_TOKEN:
            self.headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        else:
            self.headers = {}

    def _get_api_data(self) -> Dict[str, Dict[str, str]]:
        """
        Call the GitHub API and get information about our repos.

        If we're unable to get that info for any reason, return an empty dict.
        """
        repo_dict = {}
        try:
            # Fetch the data from the GitHub API
            api_data: List[dict] = httpx.get(
                self.github_api,
                headers=self.headers,
                timeout=settings.TIMEOUT_PERIOD
            ).json()
        except httpx.TimeoutException:
            log.error("Request to fetch GitHub repository metadata for timed out!")
            return repo_dict

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
        # First off, load the timestamp of the least recently updated entry.
        if settings.STATIC_BUILD:
            last_update = None
        else:
            last_update = (
                RepositoryMetadata.objects.values_list("last_updated", flat=True)
                .order_by("last_updated").first()
            )

        # If we did not retrieve any results here, we should import them!
        if last_update is None:

            # Try to get new data from the API. If it fails, we'll return an empty list.
            # In this case, we simply don't display our projects on the site.
            api_repositories = self._get_api_data()

            # Create all the repodata records in the database.
            data = [
                RepositoryMetadata(
                    repo_name=api_data["full_name"],
                    description=api_data["description"],
                    forks=api_data["forks_count"],
                    stargazers=api_data["stargazers_count"],
                    language=api_data["language"],
                )
                for api_data in api_repositories.values()
            ]

            if settings.STATIC_BUILD:
                return data
            else:
                return RepositoryMetadata.objects.bulk_create(data)

        # If the data is stale, we should refresh it.
        if (timezone.now() - last_update).seconds > self.repository_cache_ttl:
            # Try to get new data from the API. If it fails, return the cached data.
            api_repositories = self._get_api_data()

            if not api_repositories:
                return RepositoryMetadata.objects.all()

            # Update or create all RepoData objects in self.repos
            database_repositories = []
            for api_data in api_repositories.values():
                repo_data, _created = RepositoryMetadata.objects.update_or_create(
                    repo_name=api_data["full_name"],
                    defaults={
                        'repo_name': api_data["full_name"],
                        'description': api_data["description"],
                        'forks': api_data["forks_count"],
                        'stargazers': api_data["stargazers_count"],
                        'language': api_data["language"],
                    }
                )
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
