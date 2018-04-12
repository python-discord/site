# coding=utf-8
import datetime
import difflib

import requests
from flask import request, url_for
from werkzeug.exceptions import BadRequest
from werkzeug.utils import redirect

from pysite.base_route import RouteView
from pysite.constants import EDITOR_ROLES, GITHUB_TOKEN, WIKI_AUDIT_WEBHOOK
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.rst import render


class EditView(RouteView, DBMixin):
    path = "/edit/<path:page>"  # "path" means that it accepts slashes
    name = "edit"

    table_name = "wiki"
    table_primary_key = "slug"
    revision_table_name = "revisions"

    @require_roles(*EDITOR_ROLES)
    def get(self, page):
        rst = ""
        title = ""
        preview = "<p>Preview will appear here.</p>"

        obj = self.db.get(self.table_name, page)

        if obj:
            rst = obj.get("rst", "")
            title = obj.get("title", "")
            preview = obj.get("html", preview)

            if obj.get("lock_expiry") and obj.get("lock_user") != self.user_data.get("user_id"):
                lock_time = datetime.datetime.fromtimestamp(obj["lock_expiry"])
                if datetime.datetime.utcnow() < lock_time:
                    return self.render("wiki/page_in_use.html", page=page)

        lock_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        # When debug mode is enabled, login is bypassed, meaning that user_data is not present.
        if self.user_data:
            self.db.insert(self.table_name, {
                           "slug": page,
                           "lock_expiry": lock_expiry.timestamp(),
                           "lock_user": self.user_data.get("user_id")
                           },
                           conflict="update")

        return self.render("wiki/page_edit.html", page=page, rst=rst, title=title, preview=preview)

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        before = self.db.get(self.table_name, page)
        if not before:
            before = []
        else:
            if before.get("rst") is None:
                before = []
            else:
                before = before["rst"].splitlines(keepends=True)
                if len(before) == 0:
                    pass
                else:
                    if not before[-1].endswith("\n"):
                        before[-1] += "\n"  # difflib sometimes messes up if a newline is missing on last line

        rst = request.form["rst"]

        if not rst.strip():
            raise BadRequest()

        rendered = render(rst)

        obj = {
            "slug": page,
            "title": request.form["title"],
            "rst": rst,
            "html": rendered["html"],
            "headers": rendered["headers"]
        }

        self.db.insert(
            self.table_name,
            obj,
            conflict="replace"
        )

        after = obj['rst'].splitlines(keepends=True) or []
        if len(after) == 0:
            return redirect(url_for("wiki.edit", page=page), code=303)

        if not after[-1].endswith("\n"):
            after[-1] += "\n"  # Does the same thing as L57

        diff = difflib.unified_diff(before, after, fromfile="before.rst", tofile="after.rst")
        diff = "".join(diff)

        gist_payload = {
            "description": f"Changes to: {obj['title']}",
            "public": False,
            "files": {
                "changes.md": {
                    "content": f"```diff\n{diff}\n```"
                }
            }
        }

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "User-Agent": "Discord Python Wiki (https://github.com/discord-python)"
        }

        gist = requests.post("https://api.github.com/gists",
                             json=gist_payload,
                             headers=headers)

        audit_payload = {
            "username": "Wiki Updates",
            "embeds": [
                {
                    "title": "Page Edit",
                    "description": f"**{obj['title']}** was edited by **Joseph**"
                                   f".\n\n[View diff]({gist.json().get('html_url')})",
                    "color": 4165079,
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "thumbnail": {
                        "url": "https://pythondiscord.com/static/logos/logo_discord.png"
                    }
                }
            ]
        }

        if WIKI_AUDIT_WEBHOOK:
            requests.post(WIKI_AUDIT_WEBHOOK, json=audit_payload)

        # Add the post to the revisions table
        revision_payload = {
            "slug": page,
            "post": obj,
            "date": datetime.datetime.utcnow().timestamp(),
            "user": self.user_data.get("user_id")
        }

        del revision_payload["post"]["slug"]

        self.db.insert(self.revision_table_name, revision_payload)

        return redirect(url_for("wiki.page", page=page), code=303)  # Redirect, ensuring a GET

    def patch(self, page):
        current = self.db.get(self.table_name, page)
        if current.get("lock_expiry"):
            if current["lock_user"] != self.user_data.get("user_id"):
                return "", 400
            new_lock = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            self.db.insert(self.table_name, {
                "slug": page,
                "lock_expiry": new_lock.timestamp()
            }, conflict="update")
        return "", 204
