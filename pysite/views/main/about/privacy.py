from pysite.base_route import TemplateView


class PrivacyView(TemplateView):
    path = "/about/privacy"
    name = "about.privacy"
    template = "main/about/privacy.html"
