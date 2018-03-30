import logging
from uuid import uuid4, uuid5

from flask import session
from flask_dance.consumer.backend import BaseBackend
from flask_dance.contrib.discord import discord

from pysite.constants import DISCORD_API_ENDPOINT, OAUTH_DATABASE


class OauthBackend(BaseBackend):
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

    def __init__(self, manager):
        super().__init__()
        self.db = manager.db
        self.key = manager.app.secret_key
        self.db.create_table(OAUTH_DATABASE, primary_key="id")

    def get(self, *args, **kwargs):  # Not used
        pass

    def set(self, blueprint, token):

        user = self.get_user()
        sess_id = str(uuid5(uuid4(), self.key))
        self.add_user(token, user, sess_id)

    def delete(self, blueprint):  # Not used
        pass

    def add_user(self, token_data: dict, user_data: dict, session_id: str):
        session["session_id"] = session_id

        self.db.insert(
            OAUTH_DATABASE,
            {
                "id": session_id,
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": token_data["expires_at"],
                "snowflake": int(user_data["id"])
            },
            conflict="replace"
        )

        self.db.insert(
            "users",
            {"email": user_data["email"]},
            conflict="update"
        )

    def get_user(self) -> dict:
        resp = discord.get(DISCORD_API_ENDPOINT + "/users/@me")  # 'discord' is a request.Session with oauth information
        if resp.status_code != 200:
            logging.warning("Unable to get user information: " + str(resp.json()))
        return resp.json()

    def user_data(self):
        user_id = session.get("session_id")
        if user_id:  # If the user is logged in, get user info.
            creds = self.db.get(OAUTH_DATABASE, user_id)
            if creds:
                return self.db.get("users", creds["snowflake"])

    def logout(self):
        sess_id = session.get("session_id")
        if sess_id and self.db.get(OAUTH_DATABASE, sess_id):  # If user exists in db,
            self.db.delete(OAUTH_DATABASE, sess_id)           # remove them (at least, their session)
