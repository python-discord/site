import logging

from flask import jsonify

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)


class SnakeNamesView(APIView, DBMixin):
    path = "/snake_names"
    name = "api.bot.snake_names"
    table = "snake_names"

    @api_key
    def get(self):
        """
        Returns a random name from the snake_names table.

        API key must be provided as header.
        """

        log.trace("Fetching a random snake name from the snake_names table")
        question = self.db.sample(self.table, 1)[0]

        return jsonify(question)
