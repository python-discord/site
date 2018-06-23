import rethinkdb

from pysite.base_route import RouteView
from pysite.mixins import DBMixin, OAuthMixin


class JamsUserTeamListView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/my_teams"
    name = "jams.user_team_list"

    def get(self):
        # list teams a user is (or was) a part of
        if not self.user_data:
            return self.redirect_login()

        query = self.db.query("code_jam_teams").filter(
            lambda team: team["members"].contains(self.user_data["user_id"])
        ).merge(
            lambda team: {
                "members":
                    self.db.query("users")
                        .filter(lambda user: team["members"].contains(user["user_id"]))
                        .merge(lambda user: {
                            "gitlab_username":
                                self.db.query("code_jam_participants").filter({"id": user["user_id"]})
                                .coerce_to("array")[0]["gitlab_username"]
                        }).coerce_to("array"),
                "jam": self.db.query("code_jams").get(team["jam"])
            }
        ).order_by(rethinkdb.desc("jam.number"))
        teams = self.db.run(query)

        return self.render(
            "main/jams/team_list.html",
            user_teams=True,
            teams=teams
        )
