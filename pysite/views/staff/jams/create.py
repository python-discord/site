import datetime

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/create"
    name = "jams.create"
    table_name = "code_jams"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        number = self.get_next_number()
        return self.render("staff/jams/create.html", number=number)

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self):
        data = {}

        for key in REQUIRED_KEYS:
            arg = request.form.get(key)

            if not arg:
                return BadRequest()

            data[key] = arg

        data["state"] = "planning"
        data["number"] = self.get_next_number()

        # Convert given datetime strings into actual objects, adding timezones to keep rethinkdb happy
        date_start = datetime.datetime.strptime(data["date_start"], "%Y-%m-%d %H:%M")
        date_start = date_start.replace(tzinfo=datetime.timezone.utc)

        date_end = datetime.datetime.strptime(data["date_end"], "%Y-%m-%d %H:%M")
        date_end = date_end.replace(tzinfo=datetime.timezone.utc)

        data["date_start"] = date_start
        data["date_end"] = date_end

        self.db.insert(self.table_name, data)

        return redirect(url_for("staff.jams.index"))

    def get_next_number(self) -> int:
        count = self.db.run(self.table.count(), coerce=int)

        if count:
            max_num = self.db.run(self.table.max("number"))["number"]

            return max_num + 1
        return 1
