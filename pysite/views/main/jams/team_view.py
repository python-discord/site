import logging

from rethinkdb import ReqlNonExistenceError
from werkzeug.exceptions import NotFound

from pysite.base_route import RouteView
from pysite.mixins import DBMixin, OAuthMixin

log = logging.getLogger(__name__)


class JamsTeamsListView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/team/<string:team_id>"
    name = "jams.team_view"

    table_name = "code_jam_teams"

    def get(self, team_id: str):
        try:
            query = self.db.query(self.table_name).get(team_id).merge(
                lambda team: {
                    "members":
                        self.db.query("users")
                            .filter(lambda user: team["members"].contains(user["user_id"]))
                            .merge(
                            lambda user: {
                                "gitlab_username": self.db.query("code_jam_participants").filter(
                                    {"id": user["user_id"]}
                                ).coerce_to("array")[0]["gitlab_username"]
                            }
                        ).coerce_to("array"),
                    "jam":
                        self.db.query("code_jams").filter(
                            lambda jam: jam["teams"].contains(team["id"])
                        ).coerce_to("array")[0]
                }
            )

            team = self.db.run(query)
        except ReqlNonExistenceError:
            log.exception("Failed RethinkDB query")
            raise NotFound()

        return self.render(
            "main/jams/team_view.html",
            team=team
        )
