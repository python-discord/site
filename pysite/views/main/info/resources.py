# coding=utf-8
from pysite.base_route import RouteView


class ResourcesView(RouteView):
    path = "/info/resources"
    name = "info/resources"

    def get(self):
        return self.render("main/info/resources.html")
