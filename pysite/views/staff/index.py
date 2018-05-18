from pprint import pformat

from flask import current_app

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES, DEBUG_MODE, TABLE_MANAGER_ROLES
from pysite.decorators import require_roles


class StaffView(RouteView):
    path = "/"
    name = "index"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        return self.render(
            "staff/index.html", manager=self.is_table_editor(),
            app_config=pformat(current_app.config, indent=4, width=120)
        )

    def is_table_editor(self):
        if DEBUG_MODE:
            return True

        data = self.user_data

        for role in TABLE_MANAGER_ROLES:
            if role in data.get("roles", []):
                return True

        return False
