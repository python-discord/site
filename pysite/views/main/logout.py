from flask import redirect, session

from pysite.base_route import RouteView
from pysite.mixins import OauthMixin


class LogoutView(OauthMixin, RouteView):
    name = "logout"
    path = "/auth/logout"

    def get(self):
        if self.logged_in:
            # remove user's session
            del session["session_id"]
            self.logout()
        return redirect("/")
