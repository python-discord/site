# coding=utf-8
import os

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


app = WebSocketServer(
    ('', os.environ.get("WS_PORT", 8080)),
    Resource({
        "/ws/echo": EchoApplication  # Dicts are ordered in Python 3.6
    })
)

if __name__ == "__main__":
    app.serve_forever()
