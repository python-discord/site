import datetime

from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import DEBUG_MODE, EDITOR_ROLES
from pysite.mixins import DBMixin


class RevisionsListView(RouteView, DBMixin):
    path = "/history/show/<path:page>"
    name = "history.show"

    table_name = "wiki_revisions"
    table_primary_key = "id"

    def get(self, page):
        results = self.db.filter(self.table_name, lambda revision: revision["slug"] == page)
        if len(results) == 0:
            raise NotFound()

        for result in results:
            ts = datetime.datetime.fromtimestamp(result["date"])
            result["pretty_time"] = ts.strftime("%d %b %Y")

        results = sorted(results, key=lambda revision: revision["date"], reverse=True)
        return self.render("wiki/revision_list.html", page=page, revisions=results, can_edit=self.is_staff()), 200

    def is_staff(self):
        if DEBUG_MODE:
            return True
        if not self.logged_in:
            return False

        roles = self.user_data.get("roles", [])

        for role in roles:
            if role in EDITOR_ROLES:
                return True

        return False
