# coding=utf-8
import difflib

from flask import abort
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import DiffLexer

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class CompareView(RouteView, DBMixin):
    path = "/history/compare/<string:first_rev>/<string:second_rev>"
    name = "history.compare"

    table_name = "revisions"
    table_primary_key = "id"

    def get(self, first_rev, second_rev):
        before = self.db.get(self.table_name, first_rev)
        after = self.db.get(self.table_name, second_rev)

        if not before or not after:
            abort(404)

        before_text = before["post"]["rst"]
        after_text = after["post"]["rst"]

        if not before_text.endswith("\n"):
            before_text += "\n"

        if not after_text.endswith("\n"):
            after_text += "\n"

        before_text = before_text.splitlines(keepends=True)
        after_text = after_text.splitlines(keepends=True)

        if not before["slug"] == after["slug"]:
            abort(400)  # The revisions are not from the same post

        diff = difflib.unified_diff(before_text, after_text, fromfile=f"{first_rev}.rst", tofile=f"{second_rev}.rst")
        diff = "".join(diff)
        diff = highlight(diff, DiffLexer(), HtmlFormatter())
        return self.render("wiki/compare_revision.html", title=after["post"]["title"], diff=diff)
