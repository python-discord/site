import logging

from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ErrorCodes, ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin


BANNABLE_STATES = ("preparing", "running")

log = logging.getLogger(__name__)


class UserView(APIView, DBMixin):
    path = "/bot/users/complete"
    name = "bot.users.complete"

    chunks_table = "member_chunks"
    infractions_table = "code_jam_infractions"
    jams_table = "code_jams"
    oauth_table_name = "oauth_data"
    participants_table = "code_jam_participants"
    responses_table = "code_jam_responses"
    table_name = "users"
    teams_table = "code_jam_teams"

    @api_key
    @api_params(validation_type=ValidationTypes.none)
    def post(self, _):
        log.debug(f"Size of request: {len(request.data)} bytes")

        documents = self.db.get_all(self.chunks_table)
        chunks = []

        for doc in documents:
            log.info(f"Got member chunk with {len(doc['chunk'])} users")
            chunks.append(doc["chunk"])

            self.db.delete(self.chunks_table, doc["id"], durability="soft")
        self.db.sync(self.chunks_table)

        log.info(f"Got {len(chunks)} member chunks")

        data = []

        for chunk in chunks:
            data += chunk

        log.info(f"Got {len(data)} members")

        if not data:
            return self.error(ErrorCodes.bad_data_format, "No users supplied")

        deletions = 0
        oauth_deletions = 0
        profile_deletions = 0
        response_deletions = 0
        bans = 0

        user_ids = [user["user_id"] for user in data]

        # all_users = self.db.run(self.db.query(self.table_name), coerce=list)
        #
        # for user in all_users:
        #     if user["user_id"] not in user_ids:
        #         self.db.delete(self.table_name, user["user_id"], durability="soft")
        #         deletions += 1

        all_oauth_data = self.db.run(self.db.query(self.oauth_table_name), coerce=list)

        for item in all_oauth_data:
            if item["snowflake"] not in user_ids:
                user_id = item["snowflake"]

                oauth_deletions += self.db.delete(
                    self.oauth_table_name, item["id"], durability="soft", return_changes=True
                ).get("deleted", 0)
                profile_deletions += self.db.delete(
                    self.participants_table, user_id, durability="soft", return_changes=True
                ).get("deleted", 0)

                banned = False
                responses = self.db.run(
                    self.db.query(self.responses_table).filter({"snowflake": user_id}),
                    coerce=list
                )

                for response in responses:
                    jam = response["jam"]
                    jam_obj = self.db.get(self.jams_table, jam)

                    if jam_obj:
                        if jam_obj["state"] in BANNABLE_STATES:
                            banned = True

                    self.db.delete(self.responses_table, response["id"], durability="soft")
                    response_deletions += 1

                teams = self.db.run(
                    self.db.query(self.teams_table).filter(lambda row: row["members"].contains(user_id)),
                    coerce=list
                )

                for team in teams:
                    team["members"].remove(user_id)

                    self.db.insert(self.teams_table, team, conflict="replace", durability="soft")

                if banned:
                    self.db.insert(
                        self.infractions_table, {
                            "participant": user_id,
                            "reason": "Automatic ban: Removed jammer profile in the middle of a code jam",
                            "number": -1,
                            "decremented_for": []
                        }, durability="soft"
                    )
                    bans += 1

        del user_ids

        changes = self.db.insert(
            self.table_name, *data,
            conflict="update",
            durability="soft"
        )

        self.db.sync(self.infractions_table)
        self.db.sync(self.oauth_table_name)
        self.db.sync(self.participants_table)
        self.db.sync(self.responses_table)
        self.db.sync(self.table_name)
        self.db.sync(self.teams_table)

        changes["deleted"] = deletions
        changes["deleted_oauth"] = oauth_deletions
        changes["deleted_jam_profiles"] = profile_deletions
        changes["deleted_responses"] = response_deletions
        changes["jam_bans"] = bans

        return jsonify(changes)  # pragma: no cover
