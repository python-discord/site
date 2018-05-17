from pysite.base_route import TemplateView


class JamsIndexView(TemplateView):
    path = "/jams"
    name = "jams.index"
    template = "main/jams/index.html"
