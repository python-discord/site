import logging

from rethinkdb import ReqlNonExistenceError
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin

REQUIRED_KEYS = ("title", "date_start", "date_end")
log = logging.getLogger(__name__)


class StaffView(RouteView, DBMixin):
    path = "/jams/teams/<int:jam>"
    name = "jams.teams"

    table_name = "code_jam_teams"

    forms_table = "code_jam_forms"
    jams_table = "code_jams"
    participants_table = "code_jam_participants"
    questions_table = "code_jam_questions"
    responses_table = "code_jam_responses"
    users_table = "users"

    @require_roles(*ALL_STAFF_ROLES)
    def get(self, jam: int):
        try:
            query = self.db.query(self.jams_table).get(jam).merge(
                # Merge the jam document with a custom document defined below
                lambda jam_obj: {  # The lambda lets us manipulate the jam document server-side
                    "participants":
                        # Query the responses table
                        self.db.query(self.responses_table)
                            # Filter: approved responses for this jam only  # noqa: E131
                            .filter({"jam": jam_obj["number"], "approved": True})
                            # Join each response document with documents from the user table that match the user that
                            # created this response - this is the efficient way to do things, inner/outer joins
                            # are slower as they only support explicit predicates
                            .eq_join("snowflake", self.db.query(self.users_table))
                            # Remove the user ID from the left side (the response document)
                            .without({"left": ["snowflake"]})
                            .zip()  # Combine the left and right documents together
                            .order_by("username")  # Reorder the documents by username
                            .coerce_to("array"),  # Coerce the document stream into an array
                    "profiles":
                        # Query the responses table (again)
                        # We do this because RethinkDB just returns empty lists if you join on another join
                        self.db.query(self.responses_table)
                            # Filter: approved responses for this jam only  # noqa: E131
                            .filter({"jam": jam_obj["number"], "approved": True})
                            # Join each response document with documents from the participant profiles table
                            # this time
                            .eq_join("snowflake", self.db.query(self.participants_table))
                            # Remove the user ID and answers from the left side (the response document)
                            .without({"left": ["snowflake", "answers"]})
                            .zip()  # Combine the left and right documents together
                            .order_by("username")  # Reorder the documents by username
                            .coerce_to("array"),  # Coerce the document stream into an array
                    "form": self.db.query(self.forms_table).get(jam),  # Just get the correct form object
                    "teams":
                        self.db.query(self.table_name)
                            .filter(lambda team_row: jam_obj["teams"].contains(team_row["id"]))
                            .pluck(["id", "name", "members"])
                            .coerce_to("array")
                }
            )

            jam_data = self.db.run(query)
        except ReqlNonExistenceError:
            log.exception("Failed RethinkDB query")
            raise NotFound()

        questions = {}

        for question in jam_data["form"]["questions"]:
            questions[question] = self.db.get(self.questions_table, question)

        teams = {}
        participants = {}
        assigned = []

        for team in jam_data["teams"]:
            teams[team["id"]] = team

            for member in team["members"]:
                assigned.append(member)

        for user in jam_data["participants"]:
            participants[user["user_id"]] = user

        for profile in jam_data["profiles"]:
            participants[profile["id"]]["profile"] = profile

        return self.render(
            "staff/jams/teams/view.html",
            jam=jam_data, teams=teams,
            participants=participants, assigned=assigned,
            questions=questions
        )
