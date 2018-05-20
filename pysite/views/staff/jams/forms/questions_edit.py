import json

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/forms/questions/<question>"
    name = "jams.forms.questions.edit"

    questions_table = "code_jam_questions"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, question):
        question_obj = self.db.get(self.questions_table, question)

        if not question_obj:
            return NotFound()

        question_obj["data"] = question_obj.get("data", {})

        return self.render(
            "staff/jams/forms/questions_edit.html", question=question_obj
        )

    @require_roles(*ALL_STAFF_ROLES)
    @csrf
    def post(self, question):
        question_obj = self.db.get(self.questions_table, question)

        if not question_obj:
            return NotFound()

        title = request.form.get("title")
        optional = request.form.get("optional")
        question_type = request.form.get("type")

        if not title or not optional or not question_type:
            return BadRequest()

        question_obj["title"] = title
        question_obj["optional"] = optional == "optional"
        question_obj["type"] = question_type

        if question_type == "radio":
            options = request.form.get("options")

            if not options:
                return BadRequest()

            options = json.loads(options)["options"]  # No choice this time
            question_obj["data"] = {"options": options}

        elif question_type in ("number", "range", "slider"):
            question_min = request.form.get("min")
            question_max = request.form.get("max")

            if question_min is None or question_max is None:
                return BadRequest()

            question_obj["data"] = {
                "min": question_min,
                "max": question_max
            }

        self.db.insert(self.questions_table, question_obj, conflict="replace")

        return redirect(url_for("staff.jams.forms.questions"))
