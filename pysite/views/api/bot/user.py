import logging

import rethinkdb
from flask import jsonify, request
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ErrorCodes, ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

SCHEMA = Schema([
    {
        "avatar": str,
        "discriminator": str,
        "roles": [str],
        "user_id": str,
        "username": str
    }
])

GET_SCHEMA = Schema([
    {
        "user_id": str
    }
])

DELETE_SCHEMA = Schema([
    {
        "user_id": str,

        Optional("avatar"): str,
        Optional("discriminator"): str,
        Optional("roles"): [str],
        Optional("username"): str
    }
])

BANNABLE_STATES = ("preparing", "running")


class UserView(APIView, DBMixin):
    path = "/bot/users"
    name = "bot.users"

    chunks_table = "member_chunks"
    infractions_table = "code_jam_infractions"
    jams_table = "code_jams"
    oauth_table_name = "oauth_data"
    participants_table = "code_jam_participants"
    responses_table = "code_jam_responses"
    table_name = "users"
    teams_table = "code_jam_teams"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, data):
        logging.getLogger(__name__).debug(f"Size of request: {len(request.data)} bytes")

        if not data:
            return self.error(ErrorCodes.bad_data_format, "No user IDs supplied")

        data = [x["user_id"] for x in data]

        result = self.db.run(
            self.db.query(self.table_name)
            .filter(lambda document: rethinkdb.expr(data).contains(document["user_id"])),
            coerce=list
        )

        return jsonify({"data": result})  # pragma: no cover

    @api_key
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        logging.getLogger(__name__).debug(f"Size of request: {len(request.data)} bytes")

        if not data:
            return self.error(ErrorCodes.bad_data_format, "No users supplied")

        self.db.insert(self.chunks_table, {"chunk": data})

        return jsonify({"success": True})  # pragma: no cover

    @api_key
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def put(self, data):
        changes = self.db.insert(
            self.table_name, *data,
            conflict="update"
        )

        return jsonify(changes)  # pragma: no cover

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, data):
        user_ids = [user["user_id"] for user in data]

        changes = {}

        # changes = self.db.run(
        #     self.db.query(self.table_name)
        #     .get_all(*user_ids)
        #     .delete()
        # )

        oauth_deletions = self.db.run(
            self.db.query(self.oauth_table_name)
            .get_all(*user_ids, index="snowflake")
            .delete()
        ).get("deleted", 0)

        profile_deletions = self.db.run(
            self.db.query(self.participants_table)
            .get_all(*user_ids)
            .delete()
        ).get("deleted", 0)

        bans = 0
        response_deletions = 0

        for user_id in user_ids:
            banned = False
            responses = self.db.run(self.db.query(self.responses_table).filter({"snowflake": user_id}), coerce=list)

            for response in responses:
                jam = response["jam"]
                jam_obj = self.db.get(self.jams_table, jam)

                if jam_obj:
                    if jam_obj["state"] in BANNABLE_STATES:
                        banned = True

                self.db.delete(self.responses_table, response["id"])
                response_deletions += 1

            teams = self.db.run(
                self.db.query(self.teams_table).filter(lambda row: row["members"].contains(user_id)),
                coerce=list
            )

            for team in teams:
                team["members"].remove(user_id)

                self.db.insert(self.teams_table, team, conflict="replace", durability="soft")

            self.db.sync(self.teams_table)

            if banned:
                self.db.insert(
                    self.infractions_table, {
                        "participant": user_id,
                        "reason": "Automatic ban: Removed jammer profile in the middle of a code jam",
                        "number": -1,
                        "decremented_for": []
                    }
                )
                bans += 1

        changes["deleted_oauth"] = oauth_deletions
        changes["deleted_jam_profiles"] = profile_deletions
        changes["deleted_responses"] = response_deletions
        changes["jam_bans"] = bans

        return jsonify(changes)  # pragma: no cover
