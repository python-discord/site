# coding=utf-8
from flask import abort

from pysite.base_route import RouteView


class EasterEgg500(RouteView):
    path = "/500"
    name = "500"

    def get(self):
        return abort(500)
