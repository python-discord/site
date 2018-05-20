from pysite.base_route import TemplateView


class PageView(TemplateView):
    path = "/special"
    name = "special"
    template = "wiki/special.html"
