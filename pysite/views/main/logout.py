from flask import session, redirect

from pysite.base_route import RouteView


class LogoutView(RouteView):
    name = "logout"
    path = "/logout"

    def get(self):
        if session.get("session_id"):
            del session["session_id"]
        return redirect("/")
