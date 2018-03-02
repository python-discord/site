# coding=utf-8
from werkzeug.exceptions import InternalServerError

from pysite.base_route import RouteView


class EasterEgg500(RouteView):
    path = "/500"
    name = "500"

    def get(self):
        raise InternalServerError
