from pysite.base_route import RouteView


class HelpView(RouteView):
    path = "/info/help"
    name = "info.help"

    def get(self):
        return self.render("main/info/help.html")
