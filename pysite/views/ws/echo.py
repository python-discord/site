# coding=utf-8
from pysite.websockets import Websocket


class EchoWebsocket(Websocket):
    path = "/echo"
    name = "ws_echo"

    def on_open(self):
        print("Echo | WS opened.")
        self.send("Hey, welcome!")

    def on_message(self, message):
        print(f"Echo | Message: {message}")
        self.send(message)

    def on_close(self):
        print("Echo | WS closed.")
