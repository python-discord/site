from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

POST_SCHEMA = Schema({
    'log_data': [
        {
            "author": str,
            "user_id": str,
            "content": str,
            "role_id": str,
            "timestamp": str,
            "embeds": object,
            "attachments": [str],
        }
    ]
})


class LogAPIView(APIView, DBMixin):
    path = '/bot/logs'
    name = 'bot.logs_api'
    table_name = 'bot_logs'

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        """
        Receive some log_data from a bulk deletion,
        and store it in the database.

        Returns an ID which can be used to get the data
        from the /bot/clean_logs/<id> endpoint.
        """

        # Insert and return the id to use for GET
        insert = self.db.insert(
            self.table_name,
            {
                "log_data": data["log_data"]
            }
        )

        return jsonify({"log_id": insert['generated_keys'][0]})
