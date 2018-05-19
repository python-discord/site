from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]


class StaffView(RouteView, DBMixin):
    path = "/jams/forms/questions"
    name = "jams.forms.questions"

    questions_table = "code_jam_questions"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        questions = self.db.get_all(self.questions_table)

        return self.render(
            "staff/jams/forms/questions_view.html", questions=questions,
            question_ids=[q["id"] for q in questions]
        )
