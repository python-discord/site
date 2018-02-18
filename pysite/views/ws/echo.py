# coding=utf-8
import logging

from pysite.websockets import Websocket


class EchoWebsocket(Websocket):
    path = "/echo"
    name = "ws_echo"

    def __init__(self):
        self.log = logging.getLogger()

    def on_open(self):
        self.log.debug("Echo | WS opened.")
        self.send("Hey, welcome!")

    def on_message(self, message):
        self.log.debug(f"Echo | Message: {message}")
        self.send(message)

    def on_close(self):
        self.log.debug("Echo | WS closed.")
