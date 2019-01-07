from pysite.base_route import RedirectView


class GitLabView(RedirectView):
    path = "/gitlab"
    name = "gitlab"
    page = "https://github.com/python-discord/"
    code = 302
