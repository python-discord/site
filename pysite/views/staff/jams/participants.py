import logging

from rethinkdb import ReqlNonExistenceError
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ["title", "date_start", "date_end"]
log = logging.getLogger(__name__)


class StaffView(RouteView, DBMixin):
    path = "/jams/participants/<int:jam>"
    name = "jams.participants"

    forms_table = "code_jam_forms"
    participants_table = "code_jam_participants"
    questions_table = "code_jam_questions"
    responses_table = "code_jam_responses"
    table_name = "code_jams"
    users_table = "users"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam: int):
        try:
            query = self.db.query(self.table_name).get(jam).merge(
                lambda jam_obj: {
                    "participants":
                        self.db.query(self.responses_table)
                            .filter({"jam": jam_obj["number"]})
                            .eq_join("snowflake", self.db.query(self.users_table))
                            .without({"left": "snowflake"})
                            .zip()
                            .coerce_to("array")
                }
            )

            jam_data = self.db.run(query)
        except ReqlNonExistenceError:
            log.exception("Failed RethinkDB query")
            raise NotFound()

        form_obj = self.db.get(self.forms_table, jam)
        questions = {}

        if form_obj:
            for question in form_obj["questions"]:
                questions[question] = self.db.get(self.questions_table, question)

        return self.render(
            "staff/jams/participants.html",
            jam=jam_data, form=form_obj, questions=questions
        )
