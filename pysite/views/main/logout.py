from flask import redirect, session, url_for

from pysite.base_route import RouteView


class LogoutView(RouteView):
    path = "/auth/logout"
    name = "logout"

    def get(self):
        if self.logged_in:
            # remove user's session
            del session["session_id"]
            self.oauth.logout()

        return redirect(url_for("main.index"))
