from typing import Any, Dict
from weakref import ref

from flask import Blueprint
from kombu import Connection
from rethinkdb.ast import Table

from pysite.constants import (
    BOT_EVENT_QUEUE, BotEventTypes,
    RMQ_HOST, RMQ_PASSWORD, RMQ_PORT, RMQ_USERNAME
)
from pysite.database import RethinkDB
from pysite.oauth import OAuthBackend


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


class RMQMixin:
    """
    Mixin for classes that make use of RabbitMQ. It allows routes to send JSON-encoded messages to specific RabbitMQ
    queues.

    This class is intended to be mixed in alongside one of the other view classes. For example:

    >>> class MyView(APIView, RMQMixin):
    ...     name = "my_view"  # Flask internal name for this route
    ...     path = "/my_view"  # Actual URL path to reach this route
    ...     queue_name = "my_queue"  # Name of the RabbitMQ queue to send on

    Note that the queue name is optional if all you want to do is send bot events.

    This class will also work with Websockets:

    >>> class MyWebsocket(WS, RMQMixin):
    ...     name = "my_websocket"
    ...     path = "/my_websocket"
    ...     queue_name = "my_queue"
    """

    queue_name = ""

    @classmethod
    def setup(cls: "RMQMixin", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the view by calling `super().setup()` as appropriate.

        :param manager: Instance of the current RouteManager (used to get a handle for the database object)
        :param blueprint: Current Flask blueprint
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)  # pragma: no cover

    @property
    def rmq_connection(self) -> Connection:
        """
        Get a Kombu AMQP connection object - use this in a context manager so that it gets closed after you're done

        If you're just trying to send a message, check out `rmq_send` and `rmq_bot_event` instead.
        """

        return Connection(hostname=RMQ_HOST, userid=RMQ_USERNAME, password=RMQ_PASSWORD, port=RMQ_PORT)

    def rmq_send(self, data: Dict[str, Any], routing_key: str = None):
        """
        Send some data to the RabbitMQ queue

        >>> self.rmq_send(text="My hovercraft is full of eels.", source="Dirty Hungarian Phrasebook")
        >>> self.rmq_send({
        ...     "text": "My hovercraft is full of eels!",
        ...     "source": "Dirty Hungarian Phrasebook"
        ... })
        ...

        This will be delivered to the queue immediately.
        """

        if routing_key is None:
            routing_key = self.queue_name

        with self.rmq_connection as c:
            producer = c.Producer()
            producer.publish(data, routing_key=routing_key)

    def rmq_bot_event(self, event_type: BotEventTypes, data: Dict[str, Any]):
        """
        Send an event to the queue responsible for delivering events to the bot

        >>> self.rmq_bot_event(BotEventTypes.send_message, {
        ...     "channel": CHANNEL_MOD_LOG,
        ...     "message": "This is a plain-text message for @everyone, from the site!"
        ... })
        ...

        This will be delivered to the bot and actioned immediately, or when the bot comes online if it isn't already
        connected.
        """

        if not isinstance(event_type, BotEventTypes):
            raise ValueError("`event_type` must be a member of the the `pysite.constants.BotEventTypes` enum")

        return self.rmq_send(
            {"event": event_type.value, "data": data},
            routing_key=BOT_EVENT_QUEUE,
        )


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
