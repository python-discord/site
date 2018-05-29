import json
import logging

from geventwebsocket.websocket import WebSocket

from pysite.constants import BOT_API_KEY
from pysite.mixins import DBMixin
from pysite.websockets import WS


class BotWebsocket(WS, DBMixin):
    path = f"/bot/{BOT_API_KEY}"
    name = "ws.bot"
    table_name = "bot_events"
    exclusive = True

    do_changefeed = True

    def __init__(self, socket: WebSocket):
        self.log = logging.getLogger(__name__)
        super().__init__(socket)

    def on_open(self):
        self.log.debug("Bot | WS opened.")

    def on_message(self, message):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            self.send_json({"error": "Message was not valid JSON"})
            return self.socket.close()

        action = message["action"]

        if action == "login":
            if message["key"] != BOT_API_KEY:
                self.send_json({"action": "login", "result": False})
                return self.socket.close()

            self.log.debug("Bot authenticated successfully.")
            self.send_json({"action": "login", "result": True})

            self.do_changefeed = True

            for document in self.db.changes(self.table_name, include_initial=True, include_types=True):
                if not self.do_changefeed:
                    self.socket.close()
                    break

                if document["type"] not in ["add", "initial"]:
                    continue

                self.send_json({"action": "event", "event": document["new_val"]})
                self.db.run(  # Unfortunately we need to get ourselves a new connection every time
                    self.db.query(self.table_name).get(document["new_val"]["id"]).delete(),
                    new_connection=True
                )

            self.send_json({"error": "Closing..."})

        self.send_json({"error": f"Unknown action: {action}"})

    def on_close(self):
        self.log.debug("Bot | WS closed.")
        self.do_changefeed = False
