import requests
from django.shortcuts import render
from django.views import View



class Home(View):

    projects = [
        "site",
        "bot",
        "snekbox",
        "seasonalbot",
        "django-simple-bulma",
        "django-crispy-bulma",
    ]

    def _get_repo_data(self):
        """
        This will get language, stars and forks for the projects listed in Home.projects.

        Returns a dictionary with the data, in a template-friendly manner. The rate limit for
        this particular endpoint is 30 requests per minute. This should be plenty for now,
        but if we ever run into rate limiting issues, we should implement some form of caching
        for this data.
        """

        # Gotta authenticate, or we get terrible rate limits.

        # We need to query the Search API https://developer.github.com/v3/search/, using a single
        # query to query for all of the projects at the same time, and making sure we cache that data
        # and make the request no more often than once per minute or something reasonable
        # like that.

        endpoint = "https://api.github.com/search/repositories?q=" + "repo+name+separated+by+pluses"

        # And finally






    def get(self, request):

        # Call the GitHub API and ask it for some data
        return render(request, "home/index.html", {})
