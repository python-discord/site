from flask import redirect, session

from pysite.base_route import RouteView
from pysite.oauth import logout


class LogoutView(RouteView):
    name = "logout"
    path = "/logout"

    def get(self):
        if "session_id" in session:
            del session["session_id"]
            logout()
        return redirect("/")
