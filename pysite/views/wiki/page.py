# coding=utf-8
from flask import redirect, url_for
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import DEBUG_MODE, EDITOR_ROLES
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
                return redirect(url_for("wiki.edit", page=page, can_edit=False))

            raise NotFound()
        return self.render("wiki/page_view.html", page=page, data=obj, can_edit=self.is_staff())

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
