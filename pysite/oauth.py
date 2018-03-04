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
    """
    This is the backend for the oauth

    This is used to manage users that have completed
    an oauth dance. It contains 3 functions, get, set,
    and delete, however we only use set.

    Inherits:
        flake_dance.consumer.backend.BaseBackend
        pysite.mixins.DBmixin

    Properties:
        key: The app's secret, we use it too make session IDs
    """
    table_name = "oauth_data"

    def __init__(self, manager):
        global _MAIN_BACK

        super(BaseBackend, self).__init__()
        self.setup(manager, manager.oauth_blueprint)
        self.key = manager.app.secret_key
        _MAIN_BACK = self

    def get(self, *args, **kwargs):  # Not used
        pass

    def set(self, blueprint, token):
        user = get_user()  # get the user's information, based on a local proxy
        join_discord(token["access_token"], user["id"])  # Attempt to join a discord
        sess_id = str(uuid5(uuid4(), self.key))  # Create a session ID, encrypted to protect against timing attacks
        session["session_id"] = sess_id  # Set it
        self.db.insert("oauth_data", {"id": sess_id, "access_token": token["access_token"], "snowflake": user['id'],
                           "refresh_token": token["refresh_token"], "expires_at": token["expires_at"]})
        self.db.insert("users", {"user_id": user["id"], "username": user["username"],
                                 "discriminator": user["discriminator"], "email": user["email"]})
        # Insert session information into oauth_data, and user information into the user table

    def delete(self, blueprint):  # Not used
        pass


def get_user() -> dict:
    resp = discord.get(DISCORD_API_ENDPOINT + "/users/@me")  # 'discord' is a request.Session with oauth information
    if resp.status_code != 200:
        logging.warning("Unable to get user information: " + str(resp.json()))
    return resp.json()


def join_discord(token: str, snowflake: str) -> None:
    resp = requests.put(DISCORD_API_ENDPOINT + f"guilds/{SERVER_ID}/members/{snowflake}",
                        data={"access_token": token})  # Have user join our server
    if resp.status_code != 201:
        logging.warning(f"Unable to add user ({snowflake}) to server, {resp.json()}")


def user_data():
    id = session.get("session_id")
    if id and _MAIN_BACK:  # If the user is logged in, and backend exists, get the user's information
        creds = _MAIN_BACK.db.get("oauth_data", id)
        if creds:
            return _MAIN_BACK.db.get("users", creds["snowflake"])
    elif not _MAIN_BACK:
        logging.warning("Failed to get user data: _MAIN_BACK not loaded")


def logout():
    sess_id = session.get("session_id")
    if sess_id and _MAIN_BACK.db.get("oauth_data", sess_id):  # If user exists in db,
        _MAIN_BACK.delete("oauth_data", sess_id)              # remove them (at least, their session)
