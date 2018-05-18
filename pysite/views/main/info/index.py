from pysite.base_route import TemplateView


class IndexView(TemplateView):
    path = "/info/"
    name = "info.index"
    template = "main/info/index.html"
