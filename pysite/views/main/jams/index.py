import rethinkdb

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class JamsIndexView(RouteView, DBMixin):
    path = "/jams"
    name = "jams.index"
    table_name = "code_jams"

    teams_table = "code_jam_teams"

    def get(self):
        query = (
            self.db.query(self.table_name)
            .filter(rethinkdb.row["state"] != "planning")
            .merge(
                lambda jam_obj: {
                    "teams":
                        self.db.query(self.teams_table)
                            .filter(lambda team_row: jam_obj["teams"].contains(team_row["id"]))
                            .pluck(["id"])
                            .coerce_to("array")
                }
            )
            .order_by(rethinkdb.desc("number"))
            .limit(5)
        )

        jams = self.db.run(query, coerce=list)
        return self.render("main/jams/index.html", jams=jams)
