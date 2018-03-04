# coding=utf-8

from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

SCHEMA = Schema([
    {
        "user_id": int,
        "role": int
    }
])

REQUIRED_KEYS = [
    "user_id",
    "role"
]


class UserView(APIView, DBMixin):
    path = "/user"
    name = "user"
    table_name = "users"
    table_primary_key = "user_id"

    @api_key
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        changes = self.db.insert(
            self.table_name, *data,
            conflict="update"
        )

        return jsonify(changes)  # pragma: no cover
