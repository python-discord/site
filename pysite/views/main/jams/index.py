import rethinkdb

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class JamsIndexView(RouteView, DBMixin):
    path = "/jams"
    name = "jams.index"
    table_name = "code_jams"

    def get(self):
        jams = self.db.run(
            self.db.query(self.table_name).filter(rethinkdb.row["state"] != "planning").order_by("number").limit(5),
            coerce=list
        )
        print(jams)
        return self.render("main/jams/index.html", jams=jams)
