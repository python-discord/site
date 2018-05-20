from pysite.base_route import RedirectView


class JamsView(RedirectView):
    path = "/info/jams"
    name = "info.jams"
    page = "main.jams.index"
