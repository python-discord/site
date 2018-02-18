# coding=utf-8
from flask import Blueprint

from geventwebsocket.websocket import WebSocket


class WS:
    """
    Base class for representing a Websocket.

    At minimum, you must implement the `on_message(self, message)` function. Without it, you won't be able to handle
    any messages, and an error will be thrown!

    If you need access to the database, you can mix-in DBMixin, just like any view class:

    >>> class DBWebsocket(WS, DBMixin):
    ...     name = "db_websocket"
    ...     path = "/db_websocket"  # This will be prefixed with "/ws" by the blueprint
    ...     table = "ws"
    ...
    ...     def on_message(self, message):
    ...         self.send(
    ...             json.loads(self.db.get(self.table_name, message))
    ...         )

    Please note that an instance of this class is created for every websocket connected to the path. This does, however,
    mean that you can store any state required by your websocket.
    """

    path = ""  # type: str
    name = ""  # type: str

    def __init__(self, socket: WebSocket):
        self.socket = socket

    def on_open(self):
        """
        Called once when the websocket is opened. Optional.
        """

    def on_message(self, message: str):
        """
        Called when a message is received by the websocket.
        """

        raise NotImplementedError()

    def on_close(self):
        """
        Called once when the websocket is closed. Optional.
        """

    def send(self, message, binary=None):
        """
        Send a message to the currently-connected websocket, if it's open.

        Nothing will happen if the websocket is closed.
        """

        if not self.socket.closed:
            self.socket.send(message, binary=binary)

    @classmethod
    def setup(cls: "type(WS)", manager: "pysite.route_manager.RouteManager", blueprint: Blueprint):
        """
        Set up the websocket object, calling `setup()` on any superclasses as necessary (for example, on the DB
        mixin).

        This function will set up a websocket handler so that it behaves in a class-oriented way. It's up to you to
        deal with message handling yourself, however.
        """

        if hasattr(super(), "setup"):
            super().setup(manager, blueprint)

        if not cls.path or not cls.name:
            raise RuntimeError("Websockets must have both `path` and `name` defined")

        def handle(socket: WebSocket):
            """
            Wrap the current WS class, dispatching events to it as necessary. We're using gevent, so there's
            no need to worry about blocking here.
            """

            ws = cls(socket)  # Instantiate the current class, passing it the WS object

            ws.on_open()  # Call the "on_open" handler

            while not socket.closed:  # As long as the socket is open...
                message = socket.receive()  # Wait for a message

                if not socket.closed:  # If the socket didn't just close (there's always a None message on closing)
                    ws.on_message(message)  # Call the "on_message" handler

            ws.on_close()  # The socket just closed, call the "on_close" handler

        blueprint.route(cls.path)(handle)  # Register the handling function to the WS blueprint
