from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES, JAM_STATES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin


class StaffView(RouteView, DBMixin):
    path = "/jams"
    name = "jams.index"
    table_name = "code_jams"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        jams = self.db.get_all(self.table_name)
        return self.render("staff/jams/index.html", jams=jams, states=JAM_STATES)
