from pysite.base_route import TemplateView


class JamsInfoView(TemplateView):
    path = "/jams/info"
    name = "jams.info"
    template = "main/jams/info.html"
