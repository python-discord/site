from pysite.base_route import TemplateView


class IndexView(TemplateView):
    path = "/"
    name = "index"
    template = "main/index.html"
