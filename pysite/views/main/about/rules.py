from pysite.base_route import TemplateView


class RulesView(TemplateView):
    path = "/about/rules"
    name = "about.rules"
    template = "main/about/rules.html"
