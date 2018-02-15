# coding=utf-8

from flask import jsonify, request

from pysite.base_route import APIView, DBViewMixin
from pysite.constants import ErrorCodes
from pysite.decorators import valid_api_key

REQUIRED_KEYS = [
    "user_id",
    "role"
]


class UserView(APIView, DBViewMixin):
    path = "/user"
    name = "user"
    table_name = "users"
    table_primary_key = "user_id"

    @valid_api_key
    def post(self):
        data = request.get_json()

        if not isinstance(data, list):
            data = [data]

        for user in data:
            if not all(k in user for k in REQUIRED_KEYS):
                print(user)
                return self.error(ErrorCodes.missing_parameters)

            self.db.insert(
                self.table_name,
                {
                    "user_id": user["user_id"],
                    "role": user["role"],
                },
                conflict="update",
                durability="soft"
            )

        self.db.sync(self.table_name)

        return jsonify({"success": True})
