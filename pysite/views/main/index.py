# coding=utf-8
from pysite.base_route import RouteView
from pysite.constants import DISCORD_OAUTH_REDIRECT
from pysite.oauth import user_data


class IndexView(RouteView):
    path = "/"
    name = "index"

    def get(self):
        user_information = user_data()
        return self.render("main/index.html", user=user_information, login_url=DISCORD_OAUTH_REDIRECT)
