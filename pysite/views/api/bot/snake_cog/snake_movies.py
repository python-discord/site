import logging

from flask import jsonify

from pysite.base_route import APIView
from pysite.decorators import api_key
from pysite.mixins import DBMixin

log = logging.getLogger(__name__)


class SnakeMoviesView(APIView, DBMixin):
    path = "/snake_movies"
    name = "api.bot.snake_movies"
    table = "snake_movies"

    @api_key
    def get(self):
        """
        Returns a random movie from the snake_movies table.

        API key must be provided as header.
        """

        log.trace("Fetching a random snake movie from the snake_movies database")
        question = self.db.sample(self.table, 1)[0]["movie"]

        return jsonify(question)
