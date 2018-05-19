import logging

from flask import jsonify, request
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

SCHEMA = Schema([
    {
        "user_id": str,
        "roles": [str],
        "username": str,
        "discriminator": str
    }
])

DELETE_SCHEMA = Schema([
    {
        "user_id": str,
        Optional("roles"): [str],
        Optional("username"): str,
        Optional("discriminator"): str
    }
])


class UserView(APIView, DBMixin):
    path = "/user"
    name = "api.bot.user"
    table_name = "users"
    oauth_table_name = "oauth_data"
    participants_table = "code_jam_participants"

    @api_key
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        logging.getLogger(__name__).debug(f"Size of request: {len(request.data)} bytes")

        deletions = 0
        oauth_deletions = 0
        profile_deletions = 0

        user_ids = [user["user_id"] for user in data]

        all_users = self.db.run(self.db.query(self.table_name), coerce=list)

        for user in all_users:
            if user["user_id"] not in user_ids:
                self.db.delete(self.table_name, user["user_id"], durability="soft")
                deletions += 1

        all_oauth_data = self.db.run(self.db.query(self.oauth_table_name), coerce=list)

        for item in all_oauth_data:
            if item["snowflake"] not in user_ids:
                self.db.delete(self.oauth_table_name, item["id"], durability="soft")
                self.db.delete(self.participants_table, item["id"], durability="soft")
                oauth_deletions += 1
                profile_deletions += 1

        del user_ids

        changes = self.db.insert(
            self.table_name, *data,
            conflict="update",
            durability="soft"
        )

        self.db.sync(self.table_name)

        changes["deleted"] = deletions
        changes["deleted_oauth"] = oauth_deletions
        changes["deleted_jam_profiles"] = profile_deletions

        return jsonify(changes)  # pragma: no cover

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

        changes = self.db.run(
            self.db.query(self.table_name)
            .get_all(*user_ids)
            .delete()
        )

        oauth_deletions = self.db.run(
            self.db.query(self.oauth_table_name)
            .get_all(*user_ids, index="snowflake")
            .delete()
        ).get("deleted", 0)

        profile_deletions = self.db.run(
            self.db.query(self.participants_table)
            .get_all(*user_ids)
            .delete()
        )

        changes["deleted_oauth"] = oauth_deletions
        changes["deleted_jam_profiles"] = profile_deletions

        return jsonify(changes)  # pragma: no cover
