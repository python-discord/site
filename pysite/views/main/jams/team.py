from pysite.base_route import RouteView
from pysite.mixins import DBMixin, OAuthMixin


class JamsTeamView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/teams"
    name = "jams.teams_list"

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
                        }).coerce_to("array")
            }
        )
        teams = self.db.run(query)

        entries = []

        for team in teams:
            # find the jam for this team
            query = self.db.query("code_jams").filter(
                lambda jam: jam["teams"].contains(team["id"])
            )
            jam = next(self.db.run(query))
            entries.append({
                "team": team,
                "jam": jam
            })

        return self.render(
            "main/jams/teams_list.html",
            entries=entries
        )
