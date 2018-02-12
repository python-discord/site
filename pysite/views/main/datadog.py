# coding=utf-8
from flask import redirect

from pysite.base_route import RouteView


class DatadogView(RouteView):
    path = "/datadog"
    name = "datadog"

    def get(self):
        return redirect("https://p.datadoghq.com/sb/ac8680a8c-c01b556f01b96622fd4f57545b81d568")
