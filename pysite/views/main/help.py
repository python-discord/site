# coding=utf-8
from pysite.base_route import RouteView


class HelpView(RouteView):
    path = "/help"
    name = "help"

    def get(self):
        return self.render("main/help.html")
