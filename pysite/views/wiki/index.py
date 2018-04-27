from flask import url_for
from werkzeug.utils import redirect

from pysite.base_route import RouteView


class WikiView(RouteView):
    path = "/"
    name = "index"

    def get(self):
        return redirect(url_for("wiki.page", page="home"))
