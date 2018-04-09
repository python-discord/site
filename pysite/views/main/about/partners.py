# coding=utf-8
from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/about/partners"
    name = "about.partners"

    def get(self):
        return self.render("main/about/partners.html")
