# coding=utf-8
from pysite.base_route import RouteView


class RulesView(RouteView):
    path = "/info/rules"
    name = "info/rules"

    def get(self):
        return self.render("main/info/rules.html")
