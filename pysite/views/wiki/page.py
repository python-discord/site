# coding=utf-8
from pysite.base_route import RouteView


class PageView(RouteView):
    path = "/wiki/<path:page>"  # "path" means that it accepts slashes
    name = "page"

    def get(self, page):
        return self.render("wiki/index.html")
