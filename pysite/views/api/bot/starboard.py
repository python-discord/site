import datetime

from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

GET_SCHEMA = Schema({
    Optional("message_id"): str
})

POST_SCHEMA = Schema({
    "bot_message_id": str,
    "message_id": str,
    "guild_id": str,
    "channel_id": str,
    "author_id": str,
    "jump_to_url": str,
})

DELETE_BY_MESSAGE_SCHEMA = Schema({
    "message_id": str
})

DELETE_BY_BOT_MESSAGE_SCHEMA = Schema({
    "bot_message_id": str
})

AUTHOR_GET_SCHEMA = Schema({
    "author_id": str
})

DELETE_ALL_STARBOARD = Schema({})


class StarboardView(APIView, DBMixin):
    path = "/bot/starboard"
    name = "bot.starboard"
    table_name = "starboard_messages"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, data=None):
        """
        Get a list of all starred messages in the database,
        or a specific starred message by the db ID.

        Data must be passed as params, or ignored.
        API key must be provided as header.
        """

        if data:
            message = self.db.get(self.table_name, str(data["message_id"]))
            data = {"message": message}

            if message is None:
                return jsonify({"success": False})

        else:
            messages = self.db.get_all(self.table_name)
            data = {"messages": messages}

        return jsonify({"success": True, **data})

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        """
        Post an entry to the starboard database.

        Data must be provided as params.
        API key must be provided as header.
        """

        if self.db.get(self.table_name, data["message_id"]) is not None:
            response = {
                "message": "This message is already stored in the starboard"
            }
            return jsonify(response), 400

        data["starred_date"] = datetime.datetime.now(tz=datetime.timezone.utc)
        self.db.insert(self.table_name, data)

        return jsonify({"message": "ok"})

    @api_key
    @api_params(schema=DELETE_BY_MESSAGE_SCHEMA, validation_type=ValidationTypes.params)
    def delete(self, data):
        """
        Remove an entry for the starboard

        Returns 200 (ok, empty response) on success.
        Returns 400 if the given `user_id` is invalid.

        API key must be provided as header.
        Starboard entry to delete must be provided as the `message_id` parameter.
        """
        message_id = data.get("message_id")
        star_entry_exists = self.db.get(self.table_name, str(message_id))

        if star_entry_exists:
            self.db.delete(
                self.table_name,
                message_id
            )
            return "", 200
        return "", 400


class StarboardDeletionView(APIView, DBMixin):
    path = "/bot/starboard/delete"
    name = "bot.starboard.delete"
    table_name = "starboard_messages"

    @api_key
    @api_params(schema=DELETE_ALL_STARBOARD)
    def delete(self):
        """
        Remove ALL entries from the starboard

        Returns 200 (with a blank text) on success.
        Returns 400 (with error message as text) on failure.

        API key must be provided as header.
        """
        try:
            self.db.delete(self.table_name)
        except Exception as e:
            return e, 400
        return "", 200
