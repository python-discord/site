# coding=utf-8
from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles


class StaffView(RouteView):
    path = "/"
    name = "index"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        return self.render("staff/staff.html")
