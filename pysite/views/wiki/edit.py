# coding=utf-8
from flask import request, url_for
from werkzeug.utils import redirect

from pysite.base_route import RouteView
from pysite.constants import EDITOR_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.rst import render


class EditView(RouteView, DBMixin):
    path = "/edit/<path:page>"  # "path" means that it accepts slashes
    name = "edit"

    table_name = "wiki"
    table_primary_key = "slug"

    @require_roles(*EDITOR_ROLES)
    def get(self, page):
        rst = ""
        title = ""
        preview = "<p>Preview will appear here.</p>"

        obj = self.db.get(self.table_name, page)

        if obj:
            rst = obj["rst"]
            title = obj["title"]
            preview = obj["html"]

        return self.render("wiki/page_edit.html", page=page, rst=rst, title=title, preview=preview)

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        rst = request.form["rst"]
        obj = {
            "slug": page,
            "title": request.form["title"],
            "rst": rst,
            "html": render(rst)
        }

        self.db.insert(
            self.table_name,
            obj,
            conflict="replace"
        )

        return redirect(url_for("wiki.page", page=page), code=303)  # Redirect, ensuring a GET
