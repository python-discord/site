# coding=utf-8
from pysite.base_route import RouteView


class CountdownView(RouteView):
    path = "/countdown"
    name = "countdown"

    def get(self):
        return self.render("main/countdown.html")