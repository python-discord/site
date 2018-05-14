import logging

from flask import jsonify

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)


class SnakeIdiomView(APIView, DBMixin):
    path = "/snake_idioms"
    name = "api.bot.snake_idioms"
    table = "snake_idioms"

    @api_key
    def get(self):
        """
        Returns a random idiom from the snake_idioms table.

        API key must be provided as header.
        """

        log.trace("Fetching a random idiom from the snake_idioms database")
        question = self.db.sample(self.table, 1)[0]["idiom"]

        return jsonify(question)
