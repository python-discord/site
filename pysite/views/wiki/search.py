import html
import re

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.decorators import csrf
from pysite.mixins import DBMixin

STRIP_REGEX = re.compile(r"<[^<]+?>")


class SearchView(RouteView, DBMixin):
    path = "/search"  # "path" means that it accepts slashes
    name = "search"
    table_name = "wiki"
    revision_table_name = "wiki_revisions"

    def get(self):
        return self.render("wiki/search.html")

    @csrf
    def post(self):
        given_query = request.form.get("query")

        if not given_query or not given_query.strip():
            raise BadRequest()

        query = f"({re.escape(given_query)})"

        pages = self.db.filter(
            self.table_name,
            lambda doc: doc["text"].match(query)
        )

        if len(pages) == 1:
            slug = pages[0]["slug"]
            return redirect(url_for("wiki.page", page=slug), code=303)

        for obj in pages:
            text = obj["text"]

            matches = re.finditer(query, text)
            snippets = []

            for match in matches:
                start = match.start() - 50

                if start < 0:
                    start = 0

                end = match.end() + 50

                if end > len(text):
                    end = len(text)

                match_text = text[start:end]
                match_text = re.sub(query, r"<strong>\1</strong>", html.escape(match_text))

                snippets.append(match_text.replace("\n", "<br />"))

            obj["matches"] = snippets

        pages = sorted(pages, key=lambda d: d["title"])
        return self.render("wiki/search_results.html", pages=pages, query=given_query)
