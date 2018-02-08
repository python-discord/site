# coding=utf-8
from flask import jsonify

from pysite.base_route import RouteView


__author__ = "Gareth Coles"


class IndexView(RouteView):
    path = "/healthcheck"
    name = "healthcheck"

    def get(self):
        return jsonify({"status": "ok"})
