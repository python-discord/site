# coding=utf-8
from flask import redirect

from pysite.base_route import RouteView


class StatsView(RouteView):
    path = "/stats"
    name = "stats"

    def get(self):
        return redirect("https://p.datadoghq.com/sb/ac8680a8c-c01b556f01b96622fd4f57545b81d568")
