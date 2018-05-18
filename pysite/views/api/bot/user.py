import logging

from flask import jsonify, request
from schema import Schema

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


class UserView(APIView, DBMixin):
    path = "/bot/users"
    name = "bot.users"
    table_name = "users"

    @api_key
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        logging.getLogger(__name__).debug(f"Size of request: {len(request.data)} bytes")
        changes = self.db.insert(
            self.table_name, *data,
            conflict="update"
        )

        return jsonify(changes)  # pragma: no cover
