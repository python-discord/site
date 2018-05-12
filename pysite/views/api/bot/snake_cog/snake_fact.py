import logging

from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)

GET_SCHEMA = Schema([{}])


class SnakeFactView(APIView, DBMixin):
    path = "/snake_fact"
    name = "api.bot.snake_fact"
    table = "snake_facts"

    @api_key
    def get(self):
        """
        Returns a random fact from the snake_fact table.

        API key must be provided as header.
        """

        log.trace("Fetching a random fact from the snake_facts database")
        question = self.db.sample(self.table, 1)[0]["fact"]

        return jsonify(question)
