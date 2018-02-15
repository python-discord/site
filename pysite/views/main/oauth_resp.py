# coding=utf-8
import requests
from flask import redirect
from flask import request as r

from pysite.base_route import RouteView

API_ENDPOINT = 'https://discordapp.com/api/v6'


class OauthResp(RouteView):
    path = "/oauth_resp"
    name = "oauth_resp"

    def get(self):
        code = r.args.get('code')  # Get the code parameter from the URL requested
        if code is None:  # If the code was not supplied, return with a client error (400).
            return "Failed Request", 400  # TODO: Create error pages

        data = {
            'client_id': "{client_id}",  # Fill this in
            'client_secret': "{client_secret}",  # Fill this in
            'grant_type': 'client_credentials',
            'code': code,
            'redirect_uri': r.base_url
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        request = requests.post(API_ENDPOINT + '/oauth2/token', data, headers)
        resp = request.json()
        if 'access_token' not in resp:
            # There was an error, TODO: Log these errors, and do stuff with result
            return "Token Request Failed", 500
        # TODO: Add function to manager the user's tokens
        return redirect("/")
