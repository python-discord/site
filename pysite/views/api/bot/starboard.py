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

        API key must be provided as header.
        """

        if data:
            message = self.db.get(self.table_name, data["message_id"])
            data = {"message": message}

        else:
            messages = self.db.get_all(self.table_name)
            data = {"messages": messages}

        return jsonify({"success": True, **data})

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        """

        Data must be provided as params.
        API key must be provided as header.
        """

        if self.db.get(self.table_name, data["message_id"]) is not None:
            response = {
                "message": "This message is already stored in the starboard"
            }
            return jsonify(response), 400

        self.db.insert(
            self.table_name,
            {
                "message_id": data["message_id"],
                "bot_message_id": data["bot_message_id"],
                "guild_id": data["guild_id"],
                "channel_id": data["channel_id"],
                "author_id": data["author_id"],
                "jump_to_url": data["jump_to_url"],
                "starred_date": datetime.datetime.now(tz=datetime.timezone.utc)
            }
        )
        return jsonify({"message": "ok"})

    @api_key
    @api_params(schema=DELETE_BY_MESSAGE_SCHEMA, validation_type=ValidationTypes.params)
    def delete(self, data):
        """
        Remove an entry for the starboard

        API key must be provided as header.
        Board entry to delete must be provided as the `message_id` query argument.
        """
        message_id = data.get("message_id")
        star_entry_exists = self.db.get(self.table_name, message_id)

        if star_entry_exists:
            self.db.delete(
                self.table_name,
                message_id
            )
            return jsonify({"success": True})
        return jsonify({"success": False})
