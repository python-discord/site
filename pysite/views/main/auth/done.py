from flask import redirect, session, url_for

from pysite.base_route import RouteView


class AuthDoneView(RouteView):
    path = "/auth/done"
    name = "auth.done"

    def get(self):
        if self.logged_in:
            target = session.get("redirect_target")

            if target:
                del session["redirect_target"]
                return redirect(url_for(target["url"], **target.get("kwargs", {})))

        return redirect(url_for("main.index"))
