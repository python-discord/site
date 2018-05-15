from pysite.base_route import TemplateView


class IndexView(TemplateView):
    path = "/info/jams"
    name = "info.jams"
    template = "main/info/jams.html"
