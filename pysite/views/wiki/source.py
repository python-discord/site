# coding=utf-8
from flask import redirect, url_for
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import DEBUG_MODE, EDITOR_ROLES
from pysite.mixins import DBMixin


class PageView(RouteView, DBMixin):
    path = "/source/<path:page>"  # "path" means that it accepts slashes
    name = "source"
    table_name = "wiki"

    def get(self, page):
        obj = self.db.get(self.table_name, page)

        if obj is None:
            if self.is_staff():
                return redirect(url_for("wiki.edit", page=page, can_edit=False))

            raise NotFound()

        rst = obj["rst"]
        rst = highlight(rst, get_lexer_by_name("rst"), HtmlFormatter(preclass="code", linenos="inline"))
        return self.render("wiki/page_source.html", page=page, data=obj, rst=rst, can_edit=self.is_staff())

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
