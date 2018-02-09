# coding=utf-8
from pysite.base_route import RouteView


class PartnersView(RouteView):
    path = "/partners"
    name = "partners"

    def get(self):
        return self.render("partners.html")