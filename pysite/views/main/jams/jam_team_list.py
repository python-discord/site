import logging

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
        jam_obj = self.db.get(self.jams_table, jam_id)
        if not jam_obj:
            raise NotFound()

        query = self.db.query(self.table_name).get_all(self.table_name, *jam_obj["teams"]).pluck(
            ["id", "name", "members", "repo"]).merge(
            lambda team: {
                "members":
                    self.db.query("users")
                        .filter(lambda user: team["members"].contains(user["user_id"]))
                        .coerce_to("array")
            }).coerce_to("array")

        jam_obj["teams"] = self.db.run(query)

        return self.render(
            "main/jams/team_list.html",
            jam=jam_obj,
            teams=jam_obj["teams"],
            member_ids=self.member_ids
        )

    def member_ids(self, members):
        return [member["user_id"] for member in members]
