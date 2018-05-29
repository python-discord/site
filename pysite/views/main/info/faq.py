from pysite.base_route import TemplateView


class IndexView(TemplateView):
    path = "/info/faq"
    name = "info.faq"
    template = "main/info/faq.html"
