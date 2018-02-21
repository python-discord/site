# coding=utf-8
from pysite.base_route import RouteView


class StaffView(RouteView):
    path = "/"
    name = "staff"

    def get(self):
        return self.render("staff/staff.html")
