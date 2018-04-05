# coding=utf-8
from pprint import pformat

from flask import current_app

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles


class StaffView(RouteView):
    path = "/"
    name = "index"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        return self.render("staff/staff.html", app_config=pformat(current_app.config, indent=4, width=120))
