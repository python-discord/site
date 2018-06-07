from pysite.base_route import RedirectView


class GitLabView(RedirectView):
    path = "/gitlab"
    name = "gitlab"
    page = "https://gitlab.com/discord-python/"
    code = 302
