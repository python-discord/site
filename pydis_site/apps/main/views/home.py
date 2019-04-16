import requests

from django.shortcuts import render
from django.utils import timezone
from django.views import View
from pydis_site.apps.main.models import RepoData

GITHUB_API = "https://api.github.com/repos"
REPOS = [
    "python-discord/site",
    "python-discord/bot",
    "python-discord/snekbox",
    "python-discord/seasonalbot",
    "python-discord/django-simple-bulma",
    "python-discord/django-crispy-bulma",
]

# https://api.github.com/users/python-discord/repos gets all the data in one query.


class Home(View):
    def _get_repo_data(self, repo_name):
        """This will get language, stars and forks for the requested GitHub repo."""

        # Try to get the data from the cache
        try:
            repo_data = RepoData.objects.get(repo_name=repo_name)

            # If the data is older than 2 minutes, we should refresh it
            if (timezone.now() - repo_data.last_updated).seconds > 120:

                # Fetch the data from the GitHub API
                api_data = requests.get(f"{GITHUB_API}/{repo_name}")
                api_data = api_data.json()

                # Update the current object, and save it.
                repo_data.description = api_data["description"]
                repo_data.language = api_data["language"]
                repo_data.forks = api_data["forks_count"]
                repo_data.stargazers = api_data["stargazers_count"]
                repo_data.save()
                return repo_data

            # Otherwise, if the data is fresher than 2 minutes old, we should just return it.
            else:
                return repo_data

        # If this is raised, the data isn't there at all, so we'll need to create it.
        except RepoData.DoesNotExist:
            api_data = requests.get(f"{GITHUB_API}/{repo_name}")
            api_data = api_data.json()
            repo_data = RepoData(
                description=api_data["description"],
                forks=api_data["forks_count"],
                stargazers=api_data["stargazers_count"],
                language=api_data["language"],
            )
            repo_data.save()
            return repo_data

    def get(self, request):

        # Collect the repo data
        repo_data = []
        for repo in REPOS:
            repo_data.append(self._get_repo_data(repo))

        # Call the GitHub API and ask it for some data
        return render(request, "home/index.html", {"repo_data": repo_data})
