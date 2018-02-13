# coding=utf-8

from collections import OrderedDict

from geventwebsocket import Resource, WebSocketApplication, WebSocketServer


class EchoApplication(WebSocketApplication):
    def on_open(self):
        print("Connection opened")

    def on_message(self, message, **kwargs):
        print(f"<- {message}")
        self.ws.send(message)
        print(f"-> {message}")

    def on_close(self, reason):
        print(reason)


if __name__ == "__main__":
    app = WebSocketServer(
        ('', 8000),
        Resource(OrderedDict([('/ws/echo', EchoApplication)]))
    )

    app.serve_forever()
