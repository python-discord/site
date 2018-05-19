from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/infractions"
    name = "jams.infractions"

    table_name = "code_jam_infractions"
    users_table = "users"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        infractions = self.db.get_all(self.table_name)

        for document in infractions:
            user_obj = self.db.get(self.users_table, document["participant"])

            if user_obj:
                document["participant"] = user_obj

        return self.render(
            "staff/jams/infractions/view.html", infractions=infractions,
            infraction_ids=[i["id"] for i in infractions]
        )
