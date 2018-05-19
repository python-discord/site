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
        jams = self.db.run(query,coerce=list)
        print(jams)
        return self.render("main/jams/index.html", jams=jams)
