# coding=utf-8
from pysite.base_route import RouteView
from pysite.constants import DISCORD_OAUTH_REDIRECT
from pysite.mixins import OauthMixin


class IndexView(OauthMixin, RouteView):
    path = "/"
    name = "index"

    def get(self):
        return self.render("main/index.html", logged_in=self.logged_in, login_url=DISCORD_OAUTH_REDIRECT)
