import requests
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from pydis_site.apps.main.models import RepoData

GITHUB_API = "https://api.github.com/users/python-discord/repos"


class Home(View):

    def _get_api_data(self):
        """Call the GitHub API and get information about our repos."""
        repo_dict = {repo_name: {} for repo_name in settings.HOMEPAGE_REPOS}

        # Fetch the data from the GitHub API
        api_data = requests.get(GITHUB_API)
        api_data = api_data.json()

        # Process the API data into our dict
        print(f"repo_dict = {repo_dict}")
        for repo in api_data:
            full_name = repo["full_name"]

            if full_name in settings.HOMEPAGE_REPOS:
                repo_dict[full_name] = {
                    "full_name": repo["full_name"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "forks_count": repo["forks_count"],
                    "stargazers_count": repo["stargazers_count"],
                }
        print(f"repo_dict after processing = {repo_dict}")
        return repo_dict

    def _get_repo_data(self):
        """Build a list of RepoData objects that we can use to populate the front page."""

        # Try to get site data from the cache
        try:
            repo_data = RepoData.objects.get(repo_name="python-discord/site")

            # If the data is older than 2 minutes, we should refresh it. THIS PROBABLY ALWAYS FAILS?
            if (timezone.now() - repo_data.last_updated).seconds > 120:

                diff = (timezone.now() - repo_data.last_updated).seconds
                print(f"okay baby, it's old! the seconds difference comes to: {diff}")

                # Get new data from API
                api_data_container = self._get_api_data()
                repo_data_container = []

                # Update or create all RepoData objects in settings.HOMEPAGE_REPOS
                for repo_name, api_data in api_data_container.items():
                    try:
                        repo_data = RepoData.objects.get(repo_name=repo_name)
                        repo_data.description = api_data["description"]
                        repo_data.language = api_data["language"]
                        repo_data.forks = api_data["forks_count"]
                        repo_data.stargazers = api_data["stargazers_count"]
                    except RepoData.DoesNotExist:
                        repo_data = RepoData(
                            repo_name=api_data["full_name"],
                            description=api_data["description"],
                            forks=api_data["forks_count"],
                            stargazers=api_data["stargazers_count"],
                            language=api_data["language"],
                        )
                    repo_data.save()
                    repo_data_container.append(repo_data)
                return repo_data_container

            # Otherwise, if the data is fresher than 2 minutes old, we should just return it.
            else:
                return list(RepoData.objects.all())

        # If this is raised, the database has no repodata at all, we will create them all.
        except RepoData.DoesNotExist:

            # Get new data from API
            api_data_container = self._get_api_data()
            repo_data_container = []

            # Create all the repodata records in the database.
            for api_data in api_data_container.values():
                repo_data = RepoData(
                    repo_name=api_data["full_name"],
                    description=api_data["description"],
                    forks=api_data["forks_count"],
                    stargazers=api_data["stargazers_count"],
                    language=api_data["language"],
                )
                repo_data.save()
                repo_data_container.append(repo_data)

            return repo_data_container

    def get(self, request):

        # Collect the repo data
        repo_data = self._get_repo_data()

        # Call the GitHub API and ask it for some data
        return render(request, "home/index.html", {"repo_data": repo_data})
