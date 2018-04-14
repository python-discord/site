# coding=utf-8
from pysite.base_route import RouteView


class RulesView(RouteView):
    path = "/about/rules"
    name = "about.rules"

    def get(self):
        return self.render("main/about/rules.html")
