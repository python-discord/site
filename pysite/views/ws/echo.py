import logging

from geventwebsocket.websocket import WebSocket

from pysite.websockets import WS


class EchoWebsocket(WS):
    path = "/echo"
    name = "ws.echo"

    def __init__(self, socket: WebSocket):
        super().__init__(socket)
        self.log = logging.getLogger()

    def on_open(self):
        self.log.debug("Echo | WS opened.")
        self.send("Hey, welcome!")

    def on_message(self, message):
        self.log.debug(f"Echo | Message: {message}")
        self.send(message)

    def on_close(self):
        self.log.debug("Echo | WS closed.")
