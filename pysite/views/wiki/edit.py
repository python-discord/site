# coding=utf-8
import datetime
import difflib

import requests
from flask import request, url_for
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

    @require_roles(*EDITOR_ROLES)
    def get(self, page):
        rst = ""
        title = ""
        preview = "<p>Preview will appear here.</p>"

        obj = self.db.get(self.table_name, page)

        if obj:
            rst = obj["rst"]
            title = obj["title"]
            preview = obj["html"]

        return self.render("wiki/page_edit.html", page=page, rst=rst, title=title, preview=preview)

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        before = self.db.get(self.table_name, page)
        if not before:
            before = []
        else:
            before = before["rst"].splitlines(keepends=True)
            if not before[-1].endswith("\n"):
                before[-1] += "\n"  # difflib makes the output look weird if there isn't a newline on the last line

        rst = request.form["rst"]
        obj = {
            "slug": page,
            "title": request.form["title"],
            "rst": rst,
            "html": render(rst)
        }

        self.db.insert(
            self.table_name,
            obj,
            conflict="replace"
        )

        after = obj['rst'].splitlines(keepends=True) or []
        if not after[-1].endswith("\n"):
            after[-1] += "\n"  # Does same thing as L41

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

        requests.post(WIKI_AUDIT_WEBHOOK, json=audit_payload)

        return redirect(url_for("wiki.page", page=page), code=303)  # Redirect, ensuring a GET
