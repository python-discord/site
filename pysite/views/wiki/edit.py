# coding=utf-8
from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles


class EditView(RouteView):
    path = "/edit/<path:page>"  # "path" means that it accepts slashes
    name = "edit"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, page):
        return self.render("staff/staff.html")
