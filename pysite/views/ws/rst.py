# coding=utf-8
import logging

from docutils.core import publish_parts
from geventwebsocket.websocket import WebSocket

from pysite.websockets import WS


class RSTWebsocket(WS):
    path = "/rst"
    name = "ws.rst"

    def __init__(self, socket: WebSocket):
        super().__init__(socket)
        self.log = logging.getLogger()

    def on_open(self):
        self.log.debug("RST | WS opened.")
        self.send("Hey, welcome!")

    def on_message(self, message):
        self.log.debug(f"RST | Message: {message}")
        self.send(
            publish_parts(
                source=message, writer_name="html5", settings_overrides={"traceback": True}
            )["html_body"]
        )

    def on_close(self):
        self.log.debug("RST | WS closed.")
