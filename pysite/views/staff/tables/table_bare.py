from flask import redirect, url_for
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import TABLE_MANAGER_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin
from pysite.tables import TABLES


class TableView(RouteView, DBMixin):
    path = "/tables/<table>"
    name = "tables.table_bare"

    @require_roles(*TABLE_MANAGER_ROLES)
    def get(self, table):
        if table not in TABLES:
            raise NotFound()

        return redirect(url_for("staff.tables.table", table=table, page=1))
