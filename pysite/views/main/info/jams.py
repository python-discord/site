# coding=utf-8
from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/info/jams"
    name = "info.jams"

    def get(self):
        return self.render("main/info/jams.html")
