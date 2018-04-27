import json
from logging import getLogger

from pysite.base_route import RouteView

try:
    with open("static/partners.json") as fh:
        partners = json.load(fh)
except Exception:
    getLogger("Partners").exception("Failed to load partners.json")
    categories = None


class PartnersView(RouteView):
    path = "/about/partners"
    name = "about.partners"

    def get(self):
        return self.render("main/about/partners.html", partners=partners)
