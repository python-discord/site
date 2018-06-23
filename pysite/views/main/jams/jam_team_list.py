import logging

from rethinkdb import ReqlNonExistenceError
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.mixins import DBMixin, OAuthMixin

log = logging.getLogger(__name__)


class JamsTeamListView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/teams/<int:jam_id>"
    name = "jams.jam_team_list"

    table_name = "code_jam_teams"
    jams_table = "code_jams"

    def get(self, jam_id):
        try:
            query = self.db.query(self.jams_table).get(jam_id).merge(
                lambda jam_obj: {
                    "teams":
                        self.db.query(self.table_name)
                            .filter(lambda team_row: jam_obj["teams"].contains(team_row["id"]))
                            .pluck(["id", "name", "members"])
                            .merge(
                            lambda team: {
                                "members":
                                    self.db.query("users")
                                        .filter(lambda user: team["members"].contains(user["user_id"]))
                                        .coerce_to("array")
                            }).coerce_to("array")
                }
            )

            jam_data = self.db.run(query)
        except ReqlNonExistenceError:
            log.exception("Failed RethinkDB query")
            raise NotFound()

        return self.render(
            "main/jams/team_list.html",
            jam=jam_data,
            teams=jam_data["teams"],
            member_ids=self.member_ids
        )

    def member_ids(self, members):
        return [member["user_id"] for member in members]
