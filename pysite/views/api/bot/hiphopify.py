# coding=utf-8
import datetime

from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

GET_SCHEMA = Schema([
    {
        "user_id": str
    }
])

POST_SCHEMA = Schema([
    {
        "tag_name": str,
        "tag_content": str
    }
])

DELETE_SCHEMA = Schema([
    {
        "tag_name": str
    }
])


class HiphopifyView(APIView, DBMixin):
    path = "/hiphopify"
    name = "hiphopify"
    prison_table = "hiphopify"
    name_table = "hiphopify_namelist"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        """
        Check if the user is currently in hiphop-prison.

        If user is currently servin' his sentence in the big house,
        return the name stored in the forced_nick column of prison_table.

        If user cannot be found in prison, or
        if his sentence has expired, return nothing.

        Data must be provided as params.
        API key must be provided as header.
        """

        user_id = params[0].get("user_id")
        data = self.db.get(self.prison_table, user_id) or {}

        return jsonify(data)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, json_data):
        """
        Imprisons a user in hiphop-prison.

        If a forced_nick was provided by the caller, the method will force
        this nick. If not, a random hiphop nick will be selected from the
        name_table.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        pass

        # user_id = json_data[0].get("user_id")
        # duration = json_data[0].get("duration")
        # forced_nick = json_data[0].get("forced_nick")

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, json_data):
        """
        Releases a user from hiphop-prison.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        user_id = json_data[0].get("user_id")
        prisoner_data = self.db.get(self.prison_table, user_id)
        sentence_expired = datetime.datetime.now() > prisoner_data.get("end_datetime")

        if prisoner_data and not sentence_expired:
            self.db.delete(
                self.table_name,
                user_id
            )
            return jsonify({"success": True})
        elif not prisoner_data:
            return jsonify({
                "success": False,
                "error": "Prisoner not found!"
            })
        elif sentence_expired:
            return jsonify({
                "success": False,
                "error": "Prisoner has already been released!"
            })
