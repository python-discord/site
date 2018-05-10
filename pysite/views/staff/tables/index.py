from pysite.base_route import RouteView
from pysite.constants import TABLE_MANAGER_ROLES
from pysite.database import ALL_TABLES
from pysite.decorators import require_roles


class TablesView(RouteView):
    path = "/tables"
    name = "tables.index"

    @require_roles(*TABLE_MANAGER_ROLES)
    def get(self):
        return self.render("staff/tables/index.html", tables=ALL_TABLES.keys())
