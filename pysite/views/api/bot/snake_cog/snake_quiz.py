import logging

from flask import jsonify

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)


class SnakeQuizView(APIView, DBMixin):
    path = "/bot/snake_quiz"
    name = "bot.snake_quiz"
    table = "snake_quiz"

    @api_key
    def get(self):
        """
        Returns a random question from the snake_quiz table.

        API key must be provided as header.
        """

        log.trace("Fetching a random question from the snake_quiz database")
        question = self.db.sample(self.table, 1)[0]

        return jsonify(question)
