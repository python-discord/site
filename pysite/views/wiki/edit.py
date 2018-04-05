# coding=utf-8
from flask import url_for, request
from werkzeug.utils import redirect

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin


class EditView(RouteView, DBMixin):
    path = "/edit/<path:page>"  # "path" means that it accepts slashes
    name = "edit"

    table_name = "wiki"
    table_primary_key = "slug"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, page):
        rst = ""
        title = ""

        obj = self.db.get(self.table_name, page)

        if obj:
            rst = obj["rst"]
            title = obj["title"]

        return self.render("wiki/page_edit.html", page=page, rst=rst, title=title)

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self, page):
        rst = request.form["rst"]
        return redirect(url_for("wiki.page", page=page), code=303)  # Redirect, ensuring a GET
