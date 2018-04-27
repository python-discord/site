from pysite.base_route import RouteView


class IndexView(RouteView):
    path = "/about/"
    name = "about.index"

    def get(self):
        return self.render("main/about/index.html")
