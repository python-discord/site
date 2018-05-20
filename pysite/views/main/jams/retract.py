from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.decorators import csrf
from pysite.mixins import DBMixin, OAuthMixin

BANNABLE_STATES = ("preparing", "running")


class JamsProfileView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/retract"
    name = "jams.retract"

    table_name = "code_jam_participants"
    infractions_table = "code_jam_infractions"
    jams_table = "code_jams"
    responses_table = "code_jam_responses"

    def get(self):
        if not self.user_data:
            return self.redirect_login()

        user_id = self.user_data["user_id"]
        participant = self.db.get(self.table_name, user_id)

        banned = False

        if participant:
            responses = self.db.run(self.db.query(self.responses_table).filter({"snowflake": user_id}), coerce=list)

            for response in responses:
                jam = response["jam"]
                jam_obj = self.db.get(self.jams_table, jam)

                if jam_obj:
                    if jam_obj["state"] in BANNABLE_STATES:
                        banned = True
                        break

        return self.render(
            "main/jams/retract.html", participant=participant, banned=banned
        )

    @csrf
    def post(self):
        if not self.user_data:
            return self.redirect_login()

        user_id = self.user_data["user_id"]
        participant = self.db.get(self.table_name, user_id)

        if not participant:
            return BadRequest()

        banned = False

        responses = self.db.run(self.db.query(self.responses_table).filter({"snowflake": user_id}), coerce=list)

        for response in responses:
            jam = response["jam"]
            jam_obj = self.db.get(self.jams_table, jam)

            if jam_obj:
                if jam_obj["state"] in BANNABLE_STATES:
                    banned = True

            self.db.delete(self.responses_table, response["id"])

        self.db.delete(self.table_name, participant["id"])

        if banned:
            self.db.insert(
                self.infractions_table, {
                    "participant": user_id,
                    "reason": "Automatic ban: Removed jammer profile in the middle of a code jam",
                    "number": -1,
                    "decremented_for": []
                }
            )

        return self.render(
            "main/jams/retracted.html", participant=participant, banned=banned
        )
