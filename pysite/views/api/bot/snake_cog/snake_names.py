import logging

from flask import jsonify
from schema import Optional, Schema


from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)

GET_SCHEMA = Schema([
    {
        Optional("get_all"): str
    }
])


class SnakeNamesView(APIView, DBMixin):
    path = "/snake_names"
    name = "api.bot.snake_names"
    table = "snake_names"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        """
        Returns all snake names random name from the snake_names table.

        API key must be provided as header.
        """

        get_all = None

        if params:
            get_all = params[0].get("get_all")

        if get_all:
            log.trace("Returning all snake names from the snake_names table")
            snake_names = self.db.get_all(self.table)

        else:
            log.trace("Fetching a single random snake name from the snake_names table")
            snake_names = self.db.sample(self.table, 1)[0]

        return jsonify(snake_names)
