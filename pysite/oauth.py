import logging
from uuid import uuid4, uuid5

from flask import session
from flask_dance.consumer.backend import BaseBackend
from flask_dance.contrib.discord import discord
import requests

from pysite.constants import DISCORD_API_ENDPOINT, SERVER_ID
from pysite.mixins import DBMixin

_MAIN_BACK = None  # type: pysite.database.RethinkDB


class OauthBackend(BaseBackend, DBMixin):
    table_name = "oauth_data"

    def __init__(self, manager):
        global _MAIN_BACK

        super(BaseBackend, self).__init__()
        self.setup(manager, manager.oauth_blueprint)
        self.key = manager.app.secret_key
        _MAIN_BACK = self

    def get(self, *args, **kwargs):
        pass

    def set(self, blueprint, token):
        user = get_user()
        join_discord(token["access_token"], user["id"])
        sess_id = str(uuid5(uuid4(), self.key))
        session["session_id"] = sess_id
        self.table.insert({
                           "id": sess_id,
                           "access_token": token["access_token"],
                           "refresh_token": token["refresh_token"],
                           "expires_at": token["expires_at"]
                       })
        self.db.insert("users",
                       {
                           "user_id": user["id"],
                           "username": user["username"],
                           "discriminator": user["discriminator"],
                           "email": user["email"],
                       })

    def delete(self, blueprint):
        pass


def get_user() -> dict:
    resp = discord.get(DISCORD_API_ENDPOINT + "/users/@me")
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


def logout():
    sess_id = session.get("session_id")
    if sess_id and _MAIN_BACK.get("oauth_data", sess_id):
        _MAIN_BACK.delete("oauth_data", sess_id)
