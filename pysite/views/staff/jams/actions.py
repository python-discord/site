from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ALL_STAFF_ROLES, ErrorCodes
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin

ACTIONS = ["state"]
KEYS = ["action"]


class ActionView(APIView, DBMixin):
    path = "/jams/action/"
    name = "jams.action"
    table_name = "code_jams"

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def post(self):
        action = request.args.get("action")

        if action not in ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "state":
            jam = int(request.args.get("jam"))
            state = request.args.get("state")

            if not all((jam, state)):
                return self.error(ErrorCodes.incorrect_parameters)

            jam_obj = self.db.get(self.table_name, jam)
            jam_obj["state"] = state
            self.db.insert(self.table_name, jam_obj, conflict="update")

            return jsonify({})
