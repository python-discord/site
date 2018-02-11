# coding=utf-8
import json
import os

from flask import make_response, request

import requests

from pysite.base_route import APIView
from pysite.constants import ErrorCodes

ASANA_KEY = os.environ.get("ASANA_KEY")
ASANA_TOKEN = os.environ.get("ASANA_TOKEN")
ASANA_WEBHOOK = os.environ.get("ASANA_WEBHOOK")

BASE_URL = "https://app.asana.com/api/1.0"
STORY_URL = f"{BASE_URL}/stories"
TASK_URL = f"{BASE_URL}/tasks"
USER_URL = f"{BASE_URL}/users"

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
            self.send_webhook(title="Asana", description="Hook added", color=COLOUR_GREEN)
            return response

        events = request.get_json()["events"]

        for event in events:
            func_name = f"asana_{event['type']}"

            if hasattr(self, func_name):
                func = getattr(self, func_name)
            else:
                func = self.asana_unknown

            try:
                func(**event)
            except Exception as e:
                pretty_event = json.dumps(event, indent=4, sort_keys=True)

                try:
                    self.send_webhook(
                        title="Error during webhook",
                        description=f"Failed to handle webhook: {e}\n\n```json\n{pretty_event}\n```",
                        color=COLOUR_RED
                    )
                except Exception as e:
                    print(f"Fatal error sending webhook: {repr(e)}")

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
        session.close()

    def asana_story(self, *, resource, parent, created_at, user, action, type):
        session = requests.session()
        session.headers["Authorization"] = f"Bearer {ASANA_TOKEN}"

        resp = session.get(f"{STORY_URL}/{resource}")
        resp.raise_for_status()
        story = resp.json()["data"]

        if story.get("type") == "comment" and action == "added":  # New comment!
            resp = session.get(f"{TASK_URL}/{parent}")
            resp.raise_for_status()
            task = resp.json()

            resp = session.get(f"{USER_URL}/{user}")
            resp.raise_for_status()
            user = resp.json()

            if user.get("photo"):
                photo = user["photo"]["image_128x128"]
            else:
                photo = None

            if not task.get("projects"):
                self.send_webhook(
                    title=f"Comment: Unknown Project/{task['name']}",
                    description=f"{story['text']}\n\n"
                                f"No project on task - Keys: `{', '.join(task.keys())}`",
                    color=COLOUR_GREEN,
                    url=f"https://app.asana.com/0/{project['id']}/{parent}",
                    author_name=story["created_by"]["name"],
                    author_icon=photo
                )

            else:
                project = task["projects"][0]  # Just use the first project in the list

                self.send_webhook(
                    title=f"Comment: {project['name']}",
                    description=story["text"],
                    color=COLOUR_GREEN,
                    url=f"https://app.asana.com/0/{project['id']}/{parent}",
                    author_name=story["created_by"]["name"],
                    author_icon=photo
                )
        else:
            pretty_story = json.dumps(
                story,
                indent=4,
                sort_keys=True
            )

            self.send_webhook(
                title=f"Unknown story action/type: {action}/{story.get('type')}",
                description=f"```json\n{pretty_story}\n```"
            )
        session.close()

    def asana_task(self, *, resource, parent, created_at, user, action, type):
        session = requests.session()
        session.headers["Authorization"] = f"Bearer {ASANA_TOKEN}"

        resp = session.get(f"{TASK_URL}/{resource}")
        resp.raise_for_status()
        task = resp.json()

        if action == "changed":  # New comment!
            if not user:
                # ????????????????????????????
                user = {}
            else:
                resp = session.get(f"{USER_URL}/{user}")
                resp.raise_for_status()
                user = resp.json()

            if user.get("photo"):
                photo = user["photo"]["image_128x128"]
            else:
                photo = None

            if "projects" in task:
                project = task["projects"][0]  # Just use the first project in the list

                self.send_webhook(
                    title=f"Task updated: {project['name']}/{task['name']}",
                    description="What was updated? We don't know!",
                    color=COLOUR_GREEN,
                    url=f"https://app.asana.com/0/{project['id']}/{task['id']}",
                    author_name=user.get("name"),
                    author_icon=photo
                )
            else:
                self.send_webhook(
                    title=f"Task updated: Unknown Project/{task['name']}",
                    description=f"What was updated? We don't know!\n\n"
                                f"No project on task - Keys: `{', '.join(task.keys())}`",
                    color=COLOUR_GREEN,
                    author_name=user["name"],
                    author_icon=photo
                )
        else:
            pretty_task = json.dumps(
                task,
                indent=4,
                sort_keys=True
            )

            self.send_webhook(
                title=f"Unknown task action: {action}",
                description=f"```json\n{pretty_task}\n```"
            )
        session.close()

    def asana_unknown(self, *, resource, parent, created_at, user, action, type):
        pretty_event = json.dumps(
            {
                "resource": resource,
                "parent": parent,
                "created_at": created_at,
                "user": user,
                "action": action,
                "type": type
            },
            indent=4,
            sort_keys=True
        )

        self.send_webhook(
            title="Unknown event",
            description=f"```json\n{pretty_event}\n```"
        )
