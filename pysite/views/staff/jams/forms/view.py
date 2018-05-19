from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/forms/<int:jam>"
    name = "jams.forms.view"

    table_name = "code_jams"
    forms_table = "code_jam_forms"
    questions_table = "code_jam_questions"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam):
        jam_obj = self.db.get(self.table_name, jam)

        if not jam_obj:
            return NotFound()

        form_obj = self.db.get(self.forms_table, jam)

        if not form_obj:
            form_obj = {
                "number": jam,
                "questions": []
            }

            self.db.insert(self.forms_table, form_obj)

        if form_obj["questions"]:
            questions = self.db.get_all(self.questions_table, *[q for q in form_obj["questions"]])
        else:
            questions = []

        return self.render(
            "staff/jams/forms/view.html", jam=jam_obj, form=form_obj,
            questions=questions, question_ids=[q["id"] for q in questions]
        )
