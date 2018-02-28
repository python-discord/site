# coding=utf-8
from flask import abort

from pysite.base_route import RouteView


class ErrorView(RouteView):
    path = "/error/<int:code>"
    name = "error"

    def get(self, code):
        return abort(code)
