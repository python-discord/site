import logging

from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin
from pysite.utils.time import is_expired, parse_duration

log = logging.getLogger(__name__)

GET_SCHEMA = Schema({
    "user_id": str
})

POST_SCHEMA = Schema({
    "user_id": str,
    "duration": str,
    Optional("forced_nick"): str
})

DELETE_SCHEMA = Schema({
    "user_id": str
})


class HiphopifyView(APIView, DBMixin):
    path = "/bot/hiphopify"
    name = "bot.hiphopify"
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

        user_id = params.get("user_id")

        log.debug(f"Checking if user ({user_id}) is permitted to change their nickname.")
        data = self.db.get(self.prison_table, user_id) or {}

        if data and data.get("end_timestamp"):
            log.trace("User exists in the prison_table.")
            end_time = data.get("end_timestamp")
            if is_expired(end_time):
                log.trace("...But their sentence has already expired.")
                data = {}  # Return nothing if the sentence has expired.

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

        user_id = json_data.get("user_id")
        duration = json_data.get("duration")
        forced_nick = json_data.get("forced_nick")

        log.debug(f"Attempting to imprison user ({user_id}).")

        # Get random name and picture if no forced_nick was provided.
        if not forced_nick:
            log.trace("No forced_nick provided. Fetching a random rapper name and image.")
            rapper_data = self.db.sample(self.name_table, 1)[0]
            forced_nick = rapper_data.get('name')

        # If forced nick was provided, try to look up the forced_nick in the database.
        # If a match cannot be found, just default to Lil' Jon for the image.
        else:
            log.trace(f"Forced nick provided ({forced_nick}). Trying to match it with the database.")
            rapper_data = (
                self.db.get(self.name_table, forced_nick)
                or self.db.get(self.name_table, "Lil' Joseph")
            )

        image_url = rapper_data.get('image_url')
        log.trace(f"Using the nickname {forced_nick} and the image_url {image_url}.")

        # Convert duration to valid timestamp
        try:
            log.trace("Parsing the duration and converting it to a timestamp")
            end_timestamp = parse_duration(duration)
        except ValueError:
            log.warning(f"The duration could not be parsed, or was invalid. The duration was '{duration}'.")
            return jsonify({
                "success": False,
                "error_message": "Invalid duration"
            })

        log.debug("Everything seems to be in order, inserting the data into the prison_table.")
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
            "forced_nick": forced_nick,
            "image_url": image_url
        })

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, json_data):
        """
        Releases a user from hiphop-prison.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        user_id = json_data.get("user_id")

        log.debug(f"Attempting to release user ({user_id}) from hiphop-prison.")
        prisoner_data = self.db.get(self.prison_table, user_id)
        sentence_expired = None

        log.trace(f"Checking if the user ({user_id}) is currently in hiphop-prison.")
        if prisoner_data and prisoner_data.get("end_timestamp"):
            sentence_expired = is_expired(prisoner_data['end_timestamp'])

        if prisoner_data and not sentence_expired:
            log.debug("User is currently in hiphop-prison. Deleting the record and releasing the prisoner.")
            self.db.delete(
                self.prison_table,
                user_id
            )
            return jsonify({"success": True})
        elif not prisoner_data:
            log.warning(f"User ({user_id}) is not currently in hiphop-prison.")
            return jsonify({
                "success": False,
                "error_message": "User is not currently in hiphop-prison!"
            })
        elif sentence_expired:
            log.warning(f"User ({user_id}) was in hiphop-prison, but has already been released.")
            return jsonify({
                "success": False,
                "error_message": "User has already been released from hiphop-prison!"
            })
