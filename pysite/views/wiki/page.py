# coding=utf-8
from flask import redirect, url_for

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.mixins import DBMixin


class PageView(RouteView, DBMixin):
    path = "/wiki/<path:page>"  # "path" means that it accepts slashes
    name = "page"

    table_name = "wiki"
    table_primary_key = "slug"

    def get(self, page):
        obj = self.db.get(self.table_name, page)

        if obj is None:
            if self.is_staff():
                return redirect(url_for("wiki.edit", page=page))

            return self.render("wiki/page_missing.html", page=page)
        return self.render("wiki/page_view.html", page=page, data=obj)

    def is_staff(self):
        if not self.logged_in:
            return False

        roles = self.user_data.get("roles", [])

        for role in roles:
            if role in ALL_STAFF_ROLES:
                return True

        return False
