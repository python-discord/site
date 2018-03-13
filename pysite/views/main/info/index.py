# coding=utf-8
from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/info/"
    name = "info"

    def get(self):
        return self.render("main/info/index.html")
