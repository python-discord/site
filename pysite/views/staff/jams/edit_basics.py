import datetime

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/<int:jam>/edit/basics"
    name = "jams.edit.basics"
    table_name = "code_jams"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()
        return self.render("staff/jams/edit_basics.html", jam=jam_obj)

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()

        if not jam_obj["state"] == "planning":
            return BadRequest()

        for key in REQUIRED_KEYS:
            arg = request.form.get(key)

            if not arg:
                return BadRequest()

            jam_obj[key] = arg

        # Convert given datetime strings into actual objects, adding timezones to keep rethinkdb happy
        date_start = datetime.datetime.strptime(jam_obj["date_start"], "%Y-%m-%d %H:%M")
        date_start = date_start.replace(tzinfo=datetime.timezone.utc)

        date_end = datetime.datetime.strptime(jam_obj["date_end"], "%Y-%m-%d %H:%M")
        date_end = date_end.replace(tzinfo=datetime.timezone.utc)

        jam_obj["date_start"] = date_start
        jam_obj["date_end"] = date_end

        self.db.insert(self.table_name, jam_obj, conflict="replace")

        return redirect(url_for("staff.jams.index"))
