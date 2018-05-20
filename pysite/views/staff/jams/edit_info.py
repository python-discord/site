from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.rst import render

REQUIRED_KEYS = ["info_rst", "repo", "task_rst", "theme"]
ALLOWED_STATES = ["planning", "announced", "finished"]


class StaffView(RouteView, DBMixin):
    path = "/jams/<int:jam>/edit/info"
    name = "jams.edit.info"
    table_name = "code_jams"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()

        if not jam_obj["state"] in ALLOWED_STATES:
            return BadRequest()

        return self.render("staff/jams/edit_info.html", jam=jam_obj)

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()

        if not jam_obj["state"] in ALLOWED_STATES:
            return BadRequest()

        for key in REQUIRED_KEYS:
            arg = request.form.get(key)

            if not arg:
                return BadRequest()

            jam_obj[key] = arg

        jam_obj["task_html"] = render(jam_obj["task_rst"], link_headers=False)["html"]
        jam_obj["info_html"] = render(jam_obj["info_rst"], link_headers=False)["html"]

        self.db.insert(self.table_name, jam_obj, conflict="replace")

        return redirect(url_for("staff.jams.index"))
