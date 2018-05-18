from pysite.base_route import RedirectView


class WikiView(RedirectView):
    path = "/"
    name = "index"
    page = "wiki.page"
    kwargs = {"page": "home"}
