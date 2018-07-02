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

        # Get all the participants of this jam
        # Note: the group function will return a dict with user_ids as keys, however each element will be an array
        participants_query = self.db.query("users").get_all(*jam_obj["participants"], index="user_id").group("user_id")
        participants = self.db.run(participants_query)

        # Get all the teams, leaving the team members as only an array of IDs
        query = self.db.query(self.table_name).get_all(self.table_name, *jam_obj["teams"]).pluck(
            ["id", "name", "members", "repo"]).coerce_to("array")
        jam_obj["teams"] = self.db.run(query)

        # Populate each team's members using the previously queried participant list
        for team in jam_obj["teams"]:
            team["members"] = [participants[user_id][0] for user_id in team["members"]]

        return self.render(
            "main/jams/team_list.html",
            jam=jam_obj,
            teams=jam_obj["teams"],
            member_ids=self.member_ids
        )

    def member_ids(self, members):
        return [member["user_id"] for member in members]
