import json
import logging

from geventwebsocket.websocket import WebSocket

from pysite.constants import BOT_API_KEY
from pysite.mixins import DBMixin
from pysite.websockets import WS


class BotWebsocket(WS, DBMixin):
    path = "/bot"
    name = "ws.bot"
    table_name = "bot_events"

    do_changefeed = True

    def __init__(self, socket: WebSocket):
        super().__init__(socket)
        self.log = logging.getLogger()

    def on_open(self):
        self.log.debug("Bot | WS opened.")

    def on_message(self, message):
        self.log.debug(f"Bot | Message: {message}")

        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            self.send_json({"error": "Message was not valid JSON"})
            return self.socket.close()

        action = message["action"]

        if action == "login":
            if message["key"] != BOT_API_KEY:
                return self.socket.close()

            self.do_changefeed = True

            for document in self.db.changes(self.table_name, include_initial=True, include_types=True):
                if not self.do_changefeed:
                    break

                if document["type"] not in ["add", "initial"]:
                    continue

                self.send_json({"action": "event", "event": document["new_val"]})
                self.db.delete(self.table_name, document["id"])

        self.send_json({"error": f"Unknown action: {action}"})

    def on_close(self):
        self.log.debug("Bot | WS closed.")
        self.do_changefeed = False
