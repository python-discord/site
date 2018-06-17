import datetime

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import BotEventTypes, CHANNEL_MOD_LOG, EDITOR_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin, RMQMixin


class MoveView(RouteView, DBMixin, RMQMixin):
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
                    return self.render("wiki/page_in_use.html", page=page, can_edit=True)

            return self.render("wiki/page_move.html", page=page, title=title, can_edit=True)
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

        # Move all revisions for the old slug to the new slug.
        revisions = self.db.filter(self.revision_table_name, lambda revision: revision["slug"] == obj["slug"])

        for revision in revisions:
            revision["slug"] = location
            self.db.insert(self.revision_table_name, revision, conflict="update")

        obj["slug"] = location

        self.db.insert(self.table_name, obj, conflict="update")

        self.audit_log(obj)

        return redirect(url_for("wiki.page", page=location), code=303)  # Redirect, ensuring a GET

    def audit_log(self, obj):
        self.rmq_bot_event(
            BotEventTypes.send_embed,
            {
                "target": CHANNEL_MOD_LOG,
                "title": "Wiki Page Move",
                "description": f"**{obj['title']}** was moved by **{self.user_data.get('username')}** to "
                               f"**{obj['slug']}**",
                "color": 0x3F8DD7,  # Light blue
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
