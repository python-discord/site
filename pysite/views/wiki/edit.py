import datetime
import html
import re

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.constants import BotEventTypes, CHANNEL_MOD_LOG, DEBUG_MODE, EDITOR_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin, RMQMixin
from pysite.rst import render

STRIP_REGEX = re.compile(r"<[^<]+?>")


class EditView(RouteView, DBMixin, RMQMixin):
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

            current_revisions = self.db.filter(self.revision_table_name, lambda rev: rev["slug"] == page)
            sorted_revisions = sorted(current_revisions, lambda rev: rev["date"], reverse=True)

            if len(sorted_revisions) > 0:
                old_rev = sorted_revisions[0]
            else:
                old_rev = None

            new_rev = self.db.insert(self.revision_table_name, revision_payload)["generated_keys"][0]

        self.audit_log(page, new_rev, old_rev)

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

    def audit_log(self, page, new, old):
        if not old:
            link = f"https://wiki.pythondiscord.com/source/{page}"
        else:
            link = f"https://wiki.pythondiscord.com/history/compare/{old['id']}/{new}"

        self.rmq_bot_event(
            BotEventTypes.send_embed,
            {
                "target": CHANNEL_MOD_LOG,
                "title": "Page Edit",
                "description": f"**{old['post']['title']}** edited by **{self.user_data.get('username')}**. "
                               f"[View the diff here]({link})",
                "color": 0x3F8DD7,  # Light blue
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
