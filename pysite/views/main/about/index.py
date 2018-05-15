from pysite.base_route import TemplateView


class IndexView(TemplateView):
    path = "/about/"
    name = "about.index"
    template = "main/about/index.html"
