from flask import redirect, request, url_for
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.rst import render


class StaffView(RouteView, DBMixin):
    path = "/jams/form/<int:jam>/preamble"
    name = "jams.forms.preamble.edit"

    table_name = "code_jam_forms"
    jams_table = "code_jams"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam):
        jam_obj = self.db.get(self.jams_table, jam)

        if not jam_obj:
            return NotFound()

        form_obj = self.db.get(self.table_name, jam)
        return self.render("staff/jams/forms/preamble_edit.html", jam=jam_obj, form=form_obj)

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()

        form_obj = self.db.get(self.table_name, jam)

        preamble_rst = request.form.get("preamble_rst")

        form_obj["preamble_rst"] = preamble_rst
        form_obj["preamble_html"] = render(preamble_rst, link_headers=False)["html"]

        self.db.insert(self.table_name, form_obj, conflict="replace")

        return redirect(url_for("staff.jams.forms.view", jam=jam))
