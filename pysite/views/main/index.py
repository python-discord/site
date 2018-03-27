# coding=utf-8
from pysite.base_route import RouteView
from pysite.constants import DISCORD_OAUTH_REDIRECT


class IndexView(RouteView):
    path = "/"
    name = "index"

    def get(self):
        return self.render("main/index.html", login_url=DISCORD_OAUTH_REDIRECT)
