from datetime import datetime
from weakref import ref

import requests
from flask import Blueprint
from rethinkdb.ast import Table

from pysite.constants import EmbedColors, Webhooks
from pysite.database import RethinkDB
from pysite.oauth import OAuthBackend


BOT_EVENT_REQUIRED_PARAMS = {
    "mod_log": ("level", "title", "message"),
    "send_message": ("target", "message"),
    "send_embed": ("target",),
    "add_role": ("target", "role_id", "reason"),
    "remove_role": ("target", "role_id", "reason")
}


class DBMixin:
    """
    Mixin for classes that make use of RethinkDB. It can automatically create a table with the specified primary
    key using the attributes set at class-level.

    This class is intended to be mixed in alongside one of the other view classes. For example:

    >>> class MyView(APIView, DBMixin):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     table_name = "my_table"  # Name of the table to create
    ...     table_primary_key = "username"  # Primary key to set for this table

    This class will also work with Websockets:

    >>> class MyWebsocket(WS, DBMixin):
    ...     name = "my_websocket"
    ...     path = "/my_websocket"
    ...     table_name = "my_table"
    ...     table_primary_key = "username"

    You may omit `table_primary_key` and it will be defaulted to RethinkDB's default column - "id".
    """

    table_name = ""  # type: str
    table_primary_key = "id"  # type: str

    @classmethod
    def setup(cls: "DBMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by creating the table specified by the class attributes - this will also deal with multiple
        inheritance by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager (used to get a handle for the database object)
        :param blueprint: Current Flask blueprint
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        cls._db = ref(manager.db)

    @property
    def table(self) -> Table:
        return self.db.query(self.table_name)

    @property
    def db(self) -> RethinkDB:
        return self._db()


class DiscordMixin:
    """
    Mixin for the classes that need to send log messages to discord channels via webhooks.

    This class is intended to be mixed in alongside one of the other view classes. For example:

    >>> class MyView(APIView, DiscordMixin):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     default_webhook = Webhooks.devlog  # URL of the webhook to send by default

    Note that default_webhook is optional, defaulting to Webhook.devlog.
    """

    default_webhook = Webhooks.devlog

    @classmethod
    def setup(cls: "DiscordMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

    @staticmethod
    def _discord_post(url: str, embed_data: dict):
        """
        Structures the data and posts it to be sent to the discord webhook.

        :param url: The URL of the webhook to send to.
        :param embed_data: The dict representing the embed data to be added to the payload.
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "username": "Python Discord Site",
            "embeds": [embed_data]
        }
        requests.post(url, headers=headers, data=json.dumps(payload))

    @staticmethod
    def _build_embed(title: str, description: str, timestamp: str = None, color: int = None):
        """
        Builds the embed dict in the right structure for sending to the webhook.

        :param title: The title field of the embed.
        :param description: The main description text field of the embed.
        :param timestamp: The timestamp to show in the footer of the embed.
        """
        return {
            "title": title,
            "description": description,
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "color": color or EmbedColors.info
        }

    def discord_send(self, title: str, content: str, *, timestamp: str = None, color: int = None, webhook: str = None):
        url = webhook or self.default_webhook
        embed = self._build_embed(title, content, timestamp, color)
        self._discord_post(url, embed)


class OAuthMixin:
    """
    Mixin for the classes that need access to a logged in user's information. This class should be used
    to grant route's access to user information, such as name, email, id, ect.

    There will almost never be a need for someone to inherit this, as BaseView does that for you.

    This class will add 3 properties to your route:

        * logged_in (bool): True if user is registered with the site, False else wise.

        * user_data (dict): A dict that looks like this:

        {
            "user_id": Their discord ID,
            "username": Their discord username (without discriminator),
            "discriminator": Their discord discriminator,
            "email": Their email, in which is connected to discord
        }

        user_data returns None, if the user isn't logged in.

        * oauth (OAuthBackend): The instance of pysite.oauth.OAuthBackend, connected to the RouteManager.
    """

    @classmethod
    def setup(cls: "OAuthMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

        cls._oauth = ref(manager.oauth_backend)

    @property
    def logged_in(self) -> bool:
        return self.user_data is not None

    @property
    def user_data(self) -> dict:
        return self.oauth.user_data()

    @property
    def oauth(self) -> OAuthBackend:
        return self._oauth()
