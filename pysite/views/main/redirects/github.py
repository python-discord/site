from flask import redirect

from pysite.base_route import RouteView


class GitHubView(RouteView):
    path = "/github"
    name = "github"

    def get(self):
        return redirect("https://github.com/discord-python/")
