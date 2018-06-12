import datetime
import difflib
import html
import re

import requests
from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.constants import DEBUG_MODE, EDITOR_ROLES, GITHUB_TOKEN, WIKI_AUDIT_WEBHOOK
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.rst import render

STRIP_REGEX = re.compile(r"<[^<]+?>")


class EditView(RouteView, DBMixin):
    path = "/edit/<path:page>"  # "path" means that it accepts slashes
    name = "edit"
    table_name = "wiki"
    revision_table_name = "wiki_revisions"

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
                    return self.render("wiki/page_in_use.html", page=page, can_edit=True)

        lock_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

        if not DEBUG_MODE:  # If we are in debug mode we have no user logged in, therefore we can skip locking
            self.db.insert(
                self.table_name,
                {
                    "slug": page,
                    "lock_expiry": lock_expiry.timestamp(),
                    "lock_user": self.user_data.get("user_id")
                },
                conflict="update"
            )

        return self.render("wiki/page_edit.html", page=page, rst=rst, title=title, preview=preview, can_edit=True)

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        rst = request.form.get("rst")
        title = request.form["title"]

        if not rst or not rst.strip():
            raise BadRequest()

        if not title or not title.strip():
            raise BadRequest()

        rendered = render(rst)

        obj = {
            "slug": page,
            "title": request.form["title"],
            "rst": rst,
            "html": rendered["html"],
            "text": html.unescape(STRIP_REGEX.sub("", rendered["html"]).strip()),
            "headers": rendered["headers"]
        }

        self.audit_log(page, obj)

        self.db.insert(
            self.table_name,
            obj,
            conflict="replace"
        )

        if not DEBUG_MODE:
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

    @require_roles(*EDITOR_ROLES)
    @csrf
    def patch(self, page):
        current = self.db.get(self.table_name, page)
        if not current:
            return "", 404

        if current.get("lock_expiry"):  # If there is a lock present

            # If user patching is not the user with the lock end here
            if current["lock_user"] != self.user_data.get("user_id"):
                return "", 400
            new_lock = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # New lock time, 5 minutes in future
            self.db.insert(self.table_name, {
                "slug": page,
                "lock_expiry": new_lock.timestamp()
            }, conflict="update")  # Update with new lock time
        return "", 204

    def audit_log(self, page, obj):
        if WIKI_AUDIT_WEBHOOK:  # If the audit webhook is not configured there is no point processing the diff
            before = self.db.get(self.table_name, page)
            if not before:  # If this is a new page, before will be None
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

            after = obj['rst'].splitlines(keepends=True) or [""]

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
                "User-Agent": "Discord Python Wiki (https://gitlab.com/python-discord)"
            }

            gist = requests.post("https://api.github.com/gists",
                                 json=gist_payload,
                                 headers=headers)

            audit_payload = {
                "username": "Wiki Updates",
                "embeds": [
                    {
                        "title": "Page Edit",
                        "description": f"**{obj['title']}** was edited by **{self.user_data.get('username')}**"
                                       f".\n\n[View diff]({gist.json().get('html_url')})",
                        "color": 4165079,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "thumbnail": {
                            "url": "https://pythondiscord.com/static/logos/logo_discord.png"
                        }
                    }
                ]
            }

            requests.post(WIKI_AUDIT_WEBHOOK, json=audit_payload)
