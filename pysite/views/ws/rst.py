# coding=utf-8
import logging

from geventwebsocket.websocket import WebSocket

from pysite.rst import render
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

        try:
            data = render(message)["html"]
        except Exception as e:
            self.log.exception("Parsing error")
            data = str(e)

        self.send(data)

    def on_close(self):
        self.log.debug("RST | WS closed.")
