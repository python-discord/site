# coding=utf-8
import datetime
import logging

from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin
from pysite.utils.time import parse_duration

log = logging.getLogger(__name__)

GET_SCHEMA = Schema([
    {
        "user_id": str
    }
])

POST_SCHEMA = Schema([
    {
        "user_id": str,
        "duration": str,
        Optional("forced_nick"): str
    }
])

DELETE_SCHEMA = Schema([
    {
        "user_id": str
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

        user_id = json_data[0].get("user_id")
        duration = json_data[0].get("duration")
        forced_nick = json_data[0].get("forced_nick")

        # Get random name if no forced_nick was provided.
        if not forced_nick:
            forced_nick = self.db.sample(self.name_table, 1)[0]

        # Convert duration to valid timestamp
        try:
            end_timestamp = parse_duration(duration)
        except ValueError:
            return jsonify({
                "success": False,
                "error_message": "Invalid duration"
            })

        self.db.insert(
            self.prison_table,
            {
                "user_id": user_id,
                "end_timestamp": end_timestamp,
                "forced_nick": forced_nick
            },
            conflict="update"  # If it exists, update it.
        )

        return jsonify({
            "success": True,
            "end_timestamp": end_timestamp,
            "forced_nick": forced_nick
        })

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
        sentence_expired = None

        if prisoner_data and prisoner_data.get("end_datetime"):
            sentence_expired = datetime.datetime.now() > prisoner_data.get("end_datetime")

        log.debug(f"prisoner_data = {prisoner_data}")
        log.debug(f"sentence_expired = {sentence_expired}")

        if prisoner_data and not sentence_expired:
            self.db.delete(
                self.prison_table,
                user_id
            )
            return jsonify({"success": True})
        elif not prisoner_data:
            return jsonify({
                "success": False,
                "error_message": "User is not currently in hiphop-prison!"
            })
        elif sentence_expired:
            return jsonify({
                "success": False,
                "error_message": "User has already been released from hiphop-prison!"
            })
