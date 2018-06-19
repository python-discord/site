import rethinkdb

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class JamsIndexView(RouteView, DBMixin):
    path = "/jams"
    name = "jams.index"
    table_name = "code_jams"

    def get(self):
        query = (
            self.db.query(self.table_name)
            .filter(rethinkdb.row["state"] != "planning")
            .order_by(rethinkdb.desc("number"))
            .limit(5)
        )

        jams = self.db.run(query, coerce=list)
        return self.render("main/jams/index.html", jams=jams, has_applied_to_jam=has_applied_to_jam)

    def get_jam_response(self, jam, user_id):
        query = self.db.query("code_jam_responses").filter({"jam": jam, "snowflake": user_id})
        result = self.db.run(query, coerce=list)

        if result:
            return result[0]
        return None

    def has_applied_to_jam(self, jam):
        # whether the user has applied to this jam
        if not self.logged_in:
            return False
        return self.get_jam_response(jam, self.user_data["user_id"])
