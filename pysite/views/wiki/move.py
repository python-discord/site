import datetime

import requests
from flask import redirect, url_for, request
from werkzeug.exceptions import NotFound, BadRequest

from pysite.base_route import RouteView
from pysite.constants import EDITOR_ROLES, WIKI_AUDIT_WEBHOOK
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin


class MoveView(RouteView, DBMixin):
    path = "/move/<path:page>"  # "path" means that it accepts slashes
    name = "move"
    table_name = "wiki"
    revision_table_name = "wiki_revisions"

    @require_roles(*EDITOR_ROLES)
    def get(self, page):
        obj = self.db.get(self.table_name, page)

        if obj:
            title = obj.get("title", "")

            if obj.get("lock_expiry") and obj.get("lock_user") != self.user_data.get("user_id"):
                lock_time = datetime.datetime.fromtimestamp(obj["lock_expiry"])
                if datetime.datetime.utcnow() < lock_time:
                    return self.render("wiki/page_in_use.html", page=page)

            return self.render("wiki/page_move.html", page=page, title=title)
        else:
            raise NotFound()

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        location = request.form.get("location")

        if not location or not location.strip():
            raise BadRequest()

        obj = self.db.get(self.table_name, page)

        if not obj:
            raise NotFound()

        title = obj.get("title", "")
        other_obj = self.db.get(self.table_name, location)

        if other_obj:
            return self.render(
                "wiki/page_move.html", page=page, title=title,
                message=f"There's already a page at {location} - please pick a different location"
            )

        self.db.delete(self.table_name, page)

        obj["slug"] = location

        self.db.insert(self.table_name, obj, conflict="update")

        self.audit_log(obj)

        return redirect(url_for("wiki.page", page=location), code=303)  # Redirect, ensuring a GET

    def audit_log(self, obj):
        if WIKI_AUDIT_WEBHOOK:  # If the audit webhook is not configured there is no point processing it
            audit_payload = {
                "username": "Wiki Updates",
                "embeds": [
                    {
                        "title": "Page Move",
                        "description": f"**{obj['title']}** was moved by "
                                       f"**{self.user_data.get('username')}** to "
                                       f"**{obj['slug']}**",
                        "color": 4165079,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "thumbnail": {
                            "url": "https://pythondiscord.com/static/logos/logo_discord.png"
                        }
                    }
                ]
            }

            requests.post(WIKI_AUDIT_WEBHOOK, json=audit_payload)
