# coding=utf-8
import datetime

from flask import abort

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class RevisionsListView(RouteView, DBMixin):
    path = "/history/show/<string:page>"
    name = "history.show"

    table_name = "revisions"
    table_primary_key = "id"

    def get(self, page):
        results = self.db.filter(self.table_name, lambda revision: revision["slug"] == page)
        if len(results) == 0:
            abort(404)

        for result in results:
            ts = datetime.datetime.fromtimestamp(result["date"])
            result["pretty_time"] = ts.strftime("%d %b %Y")

        results = sorted(results, key=lambda revision: revision["date"], reverse=True)
        return self.render("wiki/revision_list.html", page=page, revisions=results), 200
