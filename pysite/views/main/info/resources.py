# coding=utf-8
import json
from logging import getLogger

from pysite.base_route import RouteView

try:
    with open("static/resources.json") as fh:
        categories = json.load(fh)
except Exception:
    getLogger("Resources").exception("Failed to load resources.json")
    categories = None


class ResourcesView(RouteView):
    path = "/info/resources"
    name = "info.resources"

    def get(self):
        return self.render("main/info/resources.html", categories=categories)
