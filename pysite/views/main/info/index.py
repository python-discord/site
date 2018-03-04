# coding=utf-8
from flask import redirect

from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/info/"
    name = "info"

    def get(self):
        return redirect("/info/resources")
