from operator import itemgetter

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class PageView(RouteView, DBMixin):
    path = "/special/all_pages"
    name = "special.all_pages"
    table_name = "wiki"

    def get(self):
        pages = self.db.pluck(self.table_name, "title", "slug")
        pages = sorted(pages, key=itemgetter("title"))

        letters = {}

        for page in pages:
            letter = page["title"][0].upper()

            if letter not in letters:
                letters[letter] = []

            letters[letter].append(page)

        return self.render("wiki/special_all.html", letters=letters)
