import logging

from flask import jsonify

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)


class SpecialSnakesView(APIView, DBMixin):
    path = "/bot/special_snakes"
    name = "bot.special_snakes"
    table = "special_snakes"

    @api_key
    def get(self):
        """
        Returns all special snake objects from the database

        API key must be provided as header.
        """

        log.trace("Returning all special snakes in the database")
        snake_names = self.db.get_all(self.table)

        return jsonify(snake_names)
