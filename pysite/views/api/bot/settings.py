from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

# todo: type safety
SETTINGS_KEYS_DEFAULTS = {
    "defcon_enabled": False,
    "defcon_days": 1
}

GET_SCHEMA = Schema({
    Optional("keys"): str
})


def settings_schema():
    schema_dict = {Optional(key): type(SETTINGS_KEYS_DEFAULTS[key]) for key in SETTINGS_KEYS_DEFAULTS.keys()}
    return Schema(schema_dict)


class ServerSettingsView(APIView, DBMixin):
    path = "/bot/settings"
    name = "bot.settings"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        keys_raw = None
        if params:
            keys_raw = params.get("keys")

        keys = filter(lambda key: key in SETTINGS_KEYS_DEFAULTS,
                      keys_raw.split(",")) if keys_raw else SETTINGS_KEYS_DEFAULTS.keys()

        result = {key: (self.db.get("bot_settings", key) or {}).get("value") or SETTINGS_KEYS_DEFAULTS[key] for key in
                  keys}
        return jsonify(result)

    @api_key
    @api_params(schema=settings_schema(), validation_type=ValidationTypes.json)
    def put(self, json_data):
        # update in database

        for key, value in json_data.items():
            self.db.insert("bot_settings", {
                "key": key,
                "value": value
            }, conflict="update")

        return jsonify({
            "success": True
        })
