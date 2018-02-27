# coding=utf8
from flask import redirect

from pysite.base_route import RouteView


class OathLogin(RouteView):
    path = "/oauth"
    name = "oauth"

    def get(self):
        client_id = ''

        oauth_redirect_url = f"https://discordapp.com/api/oauth2/authorize?client_id={client_id}&" \
                             "redirect_uri=https%3A%2F%2F{request.base_url}%2Foauth_resp&response_type=code&scope=email"
        return redirect(oauth_redirect_url)
