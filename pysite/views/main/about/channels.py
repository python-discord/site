from pysite.base_route import TemplateView


class ChannelsView(TemplateView):
    path = "/about/channels"
    name = "about.channels"
    template = "main/about/channels.html"
