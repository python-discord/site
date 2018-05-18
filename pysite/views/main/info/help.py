from pysite.base_route import TemplateView


class HelpView(TemplateView):
    path = "/info/help"
    name = "info.help"
    template = "main/info/help.html"
