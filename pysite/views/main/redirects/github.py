from pysite.base_route import RedirectView


class GitHubView(RedirectView):
    path = "/github"
    name = "github"
    page = "https://gitlab.com/python-discord/"
    code = 302
