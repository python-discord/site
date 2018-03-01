import logging
from uuid import uuid4

from flask import session
from flask_dance.consumer.backend import BaseBackend
from flask_dance.contrib.discord import discord

import requests

from pysite.constants import DISCORD_API_ENDPOINT, SERVER_ID
from pysite.mixins import DBMixin

_MAIN_BACK = None


class OauthBackend(BaseBackend, DBMixin):

    table_name = "oauth_data"

    def __init__(self, manager):
        global _MAIN_BACK

        super(BaseBackend, self).__init__()
        self.setup(manager, manager.oauth_blueprint)
        _MAIN_BACK = self

    def get(self, *args, **kwargs):
        pass

    def set(self, blueprint, token):
        user = get_user(discord)
        data = self.db.get("oauth_data", user["id"])
        if data is None:
            join_discord(token["access_token"], user["id"])
            sess_id = int(uuid4())
            session["session_id"] = sess_id
            self.db.insert("oauth_data",
                           {
                               "id": user["id"],
                               "username": user["username"],
                               "discriminator": user["discriminator"],
                               "email": user["email"],
                               "access_token": token["access_token"],
                               "refresh_token": token["refresh_token"],
                               "expires_at": token["expires_at"],
                               "session": sess_id
                           })
        else:
            session["session_id"] = data["session"]

    def delete(self, blueprint):
        pass


def get_user(sess: discord) -> dict:
    resp = sess.get(DISCORD_API_ENDPOINT + "/users/@me")
    if resp.status_code != 200:
        logging.warning("Unable to get user information: " + resp.json())
    return resp.json()


def join_discord(token: str, snowflake: str) -> None:
    resp = requests.put(DISCORD_API_ENDPOINT + f"guilds/{SERVER_ID}/members/{snowflake}",
                        data={"access_token": token})
    if resp.status_code != 201:
        logging.warning(f"Unable to add user ({snowflake}) to server")


def user_data():
    id = session.get("session_id")
    if id and _MAIN_BACK:
        creds = _MAIN_BACK.db.filter("oauth_data", lambda x: x["session"] == id)
        if creds:
            return creds[0]
    else:
        if not _MAIN_BACK:
            logging.warning("Failed to get user data: _MAIN_BACK not loaded")
