# coding=utf-8
from flask import jsonify

from pysite.base_route import BaseView


class IndexView(BaseView):
    path = "/healthcheck"
    name = "healthcheck"

    def get(self):
        return jsonify({"status": "ok"})
