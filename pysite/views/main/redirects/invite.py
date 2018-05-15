from pysite.base_route import RedirectView


class InviteView(RedirectView):
    path = "/invite"
    name = "invite"
    page = "https://discord.gg/8NWhsvT"
    code = 302
