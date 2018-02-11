# coding=utf-8
import json
import os

from flask import make_response, request

import requests

from pysite.base_route import APIView
from pysite.constants import ErrorCodes

ASANA_KEY = os.environ.get("ASANA_KEY")
ASANA_WEBHOOK = os.environ.get("ASANA_WEBHOOK")

COLOUR_RED = 0xFF0000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE = 0x0000FF


class IndexView(APIView):
    path = "/asana/<asana_key>"
    name = "asana"

    def post(self, asana_key):
        if asana_key != ASANA_KEY:
            return self.error(ErrorCodes.unauthorized)

        if "X-Hook-Secret" in request.headers:  # Confirm to Asana that we would like to make this hook
            response = make_response()  # type: flask.Response
            response.headers["X-Hook-Secret"] = request.headers["X-Hook-Secret"]
            return response

        events = request.get_json()["events"]

        for event in events:
            func_name = f"asana_{event['type']}_{event['action']}"

            if hasattr(self, func_name):
                func = getattr(self, func_name)
            else:
                func = self.asana_unknown

            try:
                func(**event)
            except Exception as e:
                pretty_event = json.dumps(event, indent=4, sort_key=True)

                try:
                    self.send_webhook(
                        title="Error during webhook",
                        description=f"Failed to handle webhook: {e}\n\n```json\n{pretty_event}\n```",
                        color=COLOUR_RED
                    )
                except Exception as e:
                    print(f"Fatal error sending webhook: {e}")

        return "", 200  # Empty 200 response

    def send_webhook(self, *, title, description, color=COLOUR_BLUE, url=None, author_name=None, author_icon=None):
        session = requests.session()

        embed = {
            "title": title,
            "description": description,
            "color": color
        }

        if url:
            embed["url"] = url

        if author_name:
            embed["author"] = {
                "name": author_name,
                "icon_url": author_icon
            }

        session.post(ASANA_WEBHOOK, json={"embeds": [embed]})

    def asana_unknown(self, *, resource, parent, created_at, user, action, _type):
        pretty_event = json.dumps(
            {
                "resource": resource,
                "parent": parent,
                "created_at": created_at,
                "user": user,
                "action": action,
                "type": _type
            },
            indent=4,
            sort_key=True
        )

        self.send_webhook(
            title="Unknown event",
            description=f"```json\n{pretty_event}\n```"
        )
