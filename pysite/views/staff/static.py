# coding=utf-8
from flask import send_from_directory

from pysite.base_route import RouteView
from pysite.route_manager import STATIC_PATH


class StaffView(RouteView):
    path = "/static/<path:filename>"
    name = "staff.static"

    def get(self, filename):
        return send_from_directory(
            STATIC_PATH, filename
        )
