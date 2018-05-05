from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class PageView(RouteView, DBMixin):
    path = "/special"
    name = "special"

    def get(self):
        return self.render("wiki/special.html")
