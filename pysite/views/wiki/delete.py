import datetime

from flask import redirect, url_for
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import BotEventTypes, CHANNEL_MOD_LOG, EDITOR_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin, RMQMixin


class DeleteView(RouteView, DBMixin, RMQMixin):
    path = "/delete/<path:page>"  # "path" means that it accepts slashes
    name = "delete"
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

            return self.render("wiki/page_delete.html", page=page, title=title, can_edit=True)
        else:
            raise NotFound()

    @require_roles(*EDITOR_ROLES)
    @csrf
    def post(self, page):
        obj = self.db.get(self.table_name, page)

        if not obj:
            raise NotFound()

        self.db.delete(self.table_name, page)
        self.db.delete(self.revision_table_name, page)

        revisions = self.db.filter(self.revision_table_name, lambda revision: revision["slug"] == page)

        for revision in revisions:
            self.db.delete(self.revision_table_name, revision["id"])

        self.audit_log(obj)

        return redirect(url_for("wiki.page", page="home"), code=303)  # Redirect, ensuring a GET

    def audit_log(self, obj):
        self.rmq_bot_event(
            BotEventTypes.send_embed,
            {
                "target": CHANNEL_MOD_LOG,
                "title": f"Page Deletion",
                "description": f"**{obj['title']}** was deleted by **{self.user_data.get('username')}**",
                "color": 0x3F8DD7,  # Light blue
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
