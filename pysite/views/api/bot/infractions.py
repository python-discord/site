"""
INFRACTIONS API

"GET" endpoints in this API may take the following optional parameters, depending on the endpoint:
  - active: filters infractions that are active (true), expired (false), or either (not present/any)
  - expand: expands the result data with the information about the users (slower)
  - dangling: filters infractions that are active, or inactive infractions that have not been closed manually.
  - search: filters the "reason" field to match the given RE2 query.

Infraction Schema:
  This schema is used when an infraction's data is returned.

  Root object:
    "id" (str): the UUID of the infraction.
    "inserted_at" (str): the date and time of the creation of this infraction (RFC1123 format).
    "expires_at" (str): the date and time of the expiration of this infraction (RC1123 format), may be null.
      The significance of this field being null depends on the type of infraction. Duration-based infractions
      have a "null" expiration if they are permanent. Other infraction types do not have expirations.
    "active" (bool): whether the infraction is still active. Note that the check for expiration of
      duration-based infractions is done by the API, so you should check for expiration using this "active" field.
    "user" (object): the user to which the infraction was applied.
      "user_id" (str): the Discord ID of the user.
      "username" (optional str): the username of the user. This field is only present if the query was expanded.
      "discriminator" (optional int): the username discriminator of the user. This field is only present if the
        query was expanded.
      "avatar" (optional str): the avatar URL of the user. This field is only present if the query was expanded.
    "actor" (object): the user which applied the infraction.
      This object uses the same schema as the "user" field.
    "type" (str): the type of the infraction.
    "reason" (str): the reason for the infraction.


Endpoints:

  GET /bot/infractions
    Gets a list of all infractions, regardless of type or user.
    Parameters: "active", "expand", "dangling", "search".
    This endpoint returns an array of infraction objects.

  GET /bot/infractions/user/<user_id>
    Gets a list of all infractions for a user.
    Parameters: "active", "expand", "search".
    This endpoint returns an array of infraction objects.

  GET /bot/infractions/type/<type>
    Gets a list of all infractions of the given type (ban, mute, etc.)
    Parameters: "active", "expand", "search".
    This endpoint returns an array of infraction objects.

  GET /bot/infractions/user/<user_id>/<type>
    Gets a list of all infractions of the given type for a user.
    Parameters: "active", "expand", "search".
    This endpoint returns an array of infraction objects.

  GET /bot/infractions/user/<user_id>/<type>/current
    Gets the active infraction (if any) of the given type for a user.
    Parameters: "expand".
    This endpoint returns an object with the "infraction" key, which is either set to null (no infraction)
      or the query's corresponding infraction. It will not return an infraction if the type of the infraction
      isn't duration-based (e.g. kick, warning, etc.)

  GET /bot/infractions/id/<infraction_id>
    Gets the infraction (if any) for the given ID.
    Parameters: "expand".
    This endpoint returns an object with the "infraction" key, which is either set to null (no infraction)
      or the infraction corresponding to the ID.

  POST /bot/infractions
    Creates an infraction for a user.
    Parameters (JSON payload):
      "type" (str): the type of the infraction (must be a valid infraction type).
      "reason" (str): the reason of the infraction.
      "user_id" (str): the Discord ID of the user who is being given the infraction.
      "actor_id" (str): the Discord ID of the user who submitted the infraction.
      "duration" (optional str): the duration of the infraction. This is ignored for infractions
        which are not duration-based. For other infraction types, omitting this field may imply permanence.
      "expand" (optional bool): whether to expand the infraction user data once the infraction is inserted and returned.

  PATCH /bot/infractions
    Updates an infractions.
    Parameters (JSON payload):
      "id" (str): the ID of the infraction to update.
      "reason" (optional str): if provided, the new reason for the infraction.
      "duration" (optional str): if provided, updates the expiration of the infraction to the time of UPDATING
        plus the duration. If set to null, the expiration is also set to null (may imply permanence).
      "active" (optional bool): if provided, activates or deactivates the infraction. This does not do anything
        if the infraction isn't duration-based, or if the infraction has already expired. This marks the infraction
        as closed.
      "expand" (optional bool): whether to expand the infraction user data once the infraction is updated and returned.
"""

import datetime
from typing import NamedTuple

import rethinkdb
from flask import jsonify
from schema import Optional, Or, Schema

from pysite.base_route import APIView
from pysite.constants import ErrorCodes, ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin
from pysite.utils.time import parse_duration


class InfractionType(NamedTuple):
    timed_infraction: bool  # whether the infraction is active until it expires.


RFC1123_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
EXCLUDED_FIELDS = "user_id", "actor_id", "closed", "_timed"
INFRACTION_ORDER = rethinkdb.desc("active"), rethinkdb.desc("inserted_at")

INFRACTION_TYPES = {
    "warning": InfractionType(timed_infraction=False),
    "mute": InfractionType(timed_infraction=True),
    "ban": InfractionType(timed_infraction=True),
    "kick": InfractionType(timed_infraction=False),
    "superstar": InfractionType(timed_infraction=True)  # hiphopify
}

GET_SCHEMA = Schema({
    Optional("active"): str,
    Optional("expand"): str,
    Optional("dangling"): str,
    Optional("search"): str
})

GET_ACTIVE_SCHEMA = Schema({
    Optional("expand"): str
})

CREATE_INFRACTION_SCHEMA = Schema({
    "type": lambda tp: tp in INFRACTION_TYPES,
    "reason": Or(str, None),
    "user_id": str,  # Discord user ID
    "actor_id": str,  # Discord user ID
    Optional("duration"): str,  # If not provided, may imply permanence depending on the infraction
    Optional("expand"): bool
})

UPDATE_INFRACTION_SCHEMA = Schema({
    "id": str,
    Optional("reason"): Or(str, None),
    Optional("duration"): Or(str, None),
    Optional("active"): bool
})

IMPORT_INFRACTIONS_SCHEMA = Schema([
    {
        "id": str,
        "active": bool,
        "actor": {
            "id": str
        },
        "created_at": str,
        "expires_at": Or(str, None),
        "reason": Or(str, None),
        "type": {
            "name": str
        },
        "user": {
            "id": str
        }
    }
], ignore_extra_keys=True)


class InfractionsView(APIView, DBMixin):
    path = "/bot/infractions"
    name = "bot.infractions"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params: dict = None):
        if "dangling" in params:
            return _infraction_list_filtered(self, params, {"_timed": True, "closed": False})
        else:
            return _infraction_list_filtered(self, params, {})

    @api_key
    @api_params(schema=CREATE_INFRACTION_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        deactivate_infraction_query = None

        infraction_type = data["type"]
        user_id = data["user_id"]
        actor_id = data["actor_id"]
        reason = data["reason"]
        duration_str = data.get("duration")
        expand = data.get("expand")
        expires_at = None
        inserted_at = datetime.datetime.now(tz=datetime.timezone.utc)

        if infraction_type not in INFRACTION_TYPES:
            return self.error(ErrorCodes.incorrect_parameters, "Invalid infraction type.")

        # check if the user already has an active infraction of this type
        # if so, we need to disable that infraction and create a new infraction
        if INFRACTION_TYPES[infraction_type].timed_infraction:
            active_infraction_query = \
                self.db.query(self.table_name).merge(_merge_active_check()) \
                    .filter({"user_id": user_id, "type": infraction_type, "active": True}) \
                    .limit(1).nth(0).default(None)

            active_infraction = self.db.run(active_infraction_query)
            if active_infraction:
                deactivate_infraction_query = \
                    self.db.query(self.table_name) \
                        .get(active_infraction["id"]) \
                        .update({"active": False, "closed": True})

            if duration_str:
                try:
                    expires_at = parse_duration(duration_str)
                except ValueError:
                    return self.error(
                        ErrorCodes.incorrect_parameters,
                        "Invalid duration format."
                    )

        infraction_insert_doc = {
            "actor_id": actor_id,
            "user_id": user_id,
            "type": infraction_type,
            "reason": reason,
            "inserted_at": inserted_at,
            "expires_at": expires_at
        }

        infraction_id = self.db.insert(self.table_name, infraction_insert_doc)["generated_keys"][0]

        if deactivate_infraction_query:
            self.db.run(deactivate_infraction_query)

        query = self.db.query(self.table_name).get(infraction_id) \
            .merge(_merge_expand_users(self, expand)) \
            .merge(_merge_active_check()) \
            .without(*EXCLUDED_FIELDS).default(None)
        return jsonify({
            "infraction": self.db.run(query)
        })

    @api_key
    @api_params(schema=UPDATE_INFRACTION_SCHEMA, validation_type=ValidationTypes.json)
    def patch(self, data):
        expand = data.get("expand")
        update_collection = {
            "id": data["id"]
        }

        if "reason" in data:
            update_collection["reason"] = data["reason"]

        if "active" in data:
            update_collection["active"] = data["active"]
            update_collection["closed"] = not data["active"]

        if "duration" in data:
            duration_str = data["duration"]
            if duration_str is None:
                update_collection["expires_at"] = None
            else:
                try:
                    update_collection["expires_at"] = parse_duration(duration_str)
                except ValueError:
                    return self.error(
                        ErrorCodes.incorrect_parameters,
                        "Invalid duration format."
                    )

        query_update = self.db.query(self.table_name).update(update_collection)
        result_update = self.db.run(query_update)

        if not result_update["replaced"]:
            return jsonify({
                "success": False,
                "error_message": "Unknown infraction / nothing was changed."
            })

        # return the updated infraction
        query = self.db.query(self.table_name).get(data["id"]) \
            .merge(_merge_expand_users(self, expand)) \
            .merge(_merge_active_check()) \
            .without(*EXCLUDED_FIELDS).default(None)
        infraction = self.db.run(query)

        return jsonify({
            "infraction": infraction,
            "success": True
        })


class InfractionById(APIView, DBMixin):
    path = "/bot/infractions/id/<string:infraction_id>"
    name = "bot.infractions.id"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_ACTIVE_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params, infraction_id):
        params = params or {}
        expand = parse_bool(params.get("expand"), default=False)

        query = self.db.query(self.table_name).get(infraction_id) \
            .merge(_merge_expand_users(self, expand)) \
            .merge(_merge_active_check()) \
            .without(*EXCLUDED_FIELDS).default(None)
        return jsonify({
            "infraction": self.db.run(query)
        })


class ListInfractionsByUserView(APIView, DBMixin):
    path = "/bot/infractions/user/<string:user_id>"
    name = "bot.infractions.user"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params, user_id):
        return _infraction_list_filtered(self, params, {
            "user_id": user_id
        })


class ListInfractionsByTypeView(APIView, DBMixin):
    path = "/bot/infractions/type/<string:type>"
    name = "bot.infractions.type"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params, type):
        return _infraction_list_filtered(self, params, {
            "type": type
        })


class ListInfractionsByTypeAndUserView(APIView, DBMixin):
    path = "/bot/infractions/user/<string:user_id>/<string:type>"
    name = "bot.infractions.user.type"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params, user_id, type):
        return _infraction_list_filtered(self, params, {
            "user_id": user_id,
            "type": type
        })


class CurrentInfractionByTypeAndUserView(APIView, DBMixin):
    path = "/bot/infractions/user/<string:user_id>/<string:infraction_type>/current"
    name = "bot.infractions.user.type.current"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=GET_ACTIVE_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params, user_id, infraction_type):
        params = params or {}
        expand = parse_bool(params.get("expand"), default=False)

        query_filter = {
            "user_id": user_id,
            "type": infraction_type
        }
        query = _merged_query(self, expand, query_filter).filter({
            "active": True
        }).order_by(rethinkdb.desc("data")).limit(1).nth(0).default(None)
        return jsonify({
            "infraction": self.db.run(query)
        })


class ImportRowboatInfractionsView(APIView, DBMixin):
    path = "/bot/infractions/import"
    name = "bot.infractions.import"
    table_name = "bot_infractions"

    @api_key
    @api_params(schema=IMPORT_INFRACTIONS_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        # keep track of the un-bans, to apply after the import is complete.
        unbans = []
        infractions = []

        # previously imported infractions
        imported_infractions = self.db.run(
            self.db.query(self.table_name).filter(
                lambda row: row.has_fields("legacy_rowboat_id")
            ).fold([], lambda acc, row: acc.append(row["legacy_rowboat_id"])).coerce_to("array")
        )

        for rowboat_infraction_data in data:
            legacy_rowboat_id = rowboat_infraction_data["id"]
            if legacy_rowboat_id in imported_infractions:
                continue
            infraction_type = rowboat_infraction_data["type"]["name"]
            if infraction_type == "unban":
                unbans.append(rowboat_infraction_data)
                continue
            # adjust infraction types
            if infraction_type == "tempmute":
                infraction_type = "mute"
            if infraction_type == "tempban":
                infraction_type = "ban"
            if infraction_type not in INFRACTION_TYPES:
                # unknown infraction type
                continue
            active = rowboat_infraction_data["active"]
            reason = rowboat_infraction_data["reason"] or "<No reason>"
            user_id = rowboat_infraction_data["user"]["id"]
            actor_id = rowboat_infraction_data["actor"]["id"]
            inserted_at_str = rowboat_infraction_data["created_at"]
            try:
                inserted_at = parse_rfc1123(inserted_at_str)
            except ValueError:
                continue
            expires_at_str = rowboat_infraction_data["expires_at"]
            if expires_at_str is not None:
                try:
                    expires_at = parse_rfc1123(expires_at_str)
                except ValueError:
                    continue
            else:
                expires_at = None
            infractions.append({
                "legacy_rowboat_id": legacy_rowboat_id,
                "active": active,
                "reason": reason,
                "user_id": user_id,
                "actor_id": actor_id,
                "inserted_at": inserted_at,
                "expires_at": expires_at,
                "type": infraction_type
            })

        insertion_query = self.db.query(self.table_name).insert(infractions)
        inserted_count = self.db.run(insertion_query)["inserted"]

        # apply unbans
        for unban_data in unbans:
            inserted_at_str = unban_data["created_at"]
            user_id = unban_data["user"]["id"]
            try:
                inserted_at = parse_rfc1123(inserted_at_str)
            except ValueError:
                continue
            self.db.run(
                self.db.query(self.table_name).filter(
                    lambda row: (row["user_id"].eq(user_id)) &
                                (row["type"].eq("ban")) &
                                (row["inserted_at"] < inserted_at)
                ).pluck("id").merge(lambda row: {
                    "active": False
                }).coerce_to("array").for_each(lambda doc: self.db.query(self.table_name).get(doc["id"]).update(doc))
            )

        return jsonify({
            "success": True,
            "inserted_count": inserted_count
        })


def _infraction_list_filtered(view, params=None, query_filter=None):
    params = params or {}
    query_filter = query_filter or {}
    active = parse_bool(params.get("active"))
    expand = parse_bool(params.get("expand"), default=False)
    search = params.get("search")

    if active is not None:
        query_filter["active"] = active

    query = _merged_query(view, expand, query_filter)

    if search is not None:
        query = query.filter(
            lambda row: rethinkdb.branch(
                row["reason"].eq(None),
                False,
                row["reason"].match(search)
            )
        )

    query = query.order_by(*INFRACTION_ORDER)

    return jsonify(view.db.run(query.coerce_to("array")))


def _merged_query(view, expand, query_filter):
    return view.db.query(view.table_name).merge(_merge_active_check()).filter(query_filter) \
        .merge(_merge_expand_users(view, expand)).without(*EXCLUDED_FIELDS)


def _merge_active_check():
    # Checks if the "closed" field has been set to true (manual infraction removal).
    # If not, the "active" field is set to whether the infraction has expired.
    def _merge(row):
        return {
            "active":
                rethinkdb.branch(
                    _is_timed_infraction(row["type"]),
                    rethinkdb.branch(
                        (row["closed"].default(False).eq(True)) | (row["active"].default(True).eq(False)),
                        False,
                        rethinkdb.branch(
                            row["expires_at"].eq(None),
                            True,
                            row["expires_at"] > rethinkdb.now()
                        )
                    ),
                    False
                ),
            "closed": row["closed"].default(False),
            "_timed": _is_timed_infraction(row["type"])
        }

    return _merge


def _merge_expand_users(view, expand):
    def _do_expand(user_id):
        if not user_id:
            return None
        # Expands the user information, if it is in the database.

        if expand:
            return view.db.query("users").get(user_id).default({
                "user_id": user_id
            })

        return {
            "user_id": user_id
        }

    def _merge(row):
        return {
            "user": _do_expand(row["user_id"].default(None)),
            "actor": _do_expand(row["actor_id"].default(None))
        }

    return _merge


def _is_timed_infraction(type_var):
    # this method generates an ReQL expression to check if the given type
    # is a "timed infraction" (i.e it can expire or be permanent)

    timed_infractions = filter(lambda key: INFRACTION_TYPES[key].timed_infraction, INFRACTION_TYPES.keys())
    expr = rethinkdb.expr(False)
    for infra_type in timed_infractions:
        expr = expr | type_var.eq(infra_type)
    return expr


def parse_rfc1123(time_str):
    return datetime.datetime.strptime(time_str, RFC1123_FORMAT).replace(tzinfo=datetime.timezone.utc)


def parse_bool(a_string, default=None):
    # Not present, null or any: returns default (defaults to None)
    # false, no, or 0: returns False
    # anything else: True
    if a_string is None or a_string == "null" or a_string == "any":
        return default
    if a_string.lower() == "false" or a_string.lower() == "no" or a_string == "0":
        return False
    return True
