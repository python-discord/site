import random

from flask import jsonify, request
from schema import And, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin


OFF_TOPIC_NAME = And(
    str,
    len,
    lambda name: all(c.isalnum() or c in '-’' for c in name),
    str.islower,
    lambda name: len(name) <= 96,
    error=(
        "The channel name must be a non-blank string consisting only of"
        " lowercase regular characters, '’' and '-' with a maximum length of 96"
    )
)

DELETE_SCHEMA = Schema({
    'name': OFF_TOPIC_NAME
})

POST_SCHEMA = Schema({
    'name': OFF_TOPIC_NAME
})


class OffTopicNamesView(APIView, DBMixin):
    path = "/bot/off-topic-names"
    name = "bot.off_topic_names"
    table_name = "off_topic_names"

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.params)
    def delete(self, params):
        """
        Removes a single off-topic name from the database.
        Returns the result of the deletion call.

        API key must be provided as header.
        Name to delete must be provided as the `name` query argument.
        """

        result = self.db.delete(
            self.table_name,
            params['name'],
            return_changes=True
        )

        return jsonify(result)

    @api_key
    def get(self):
        """
        Fetch all known off-topic channel names from the database.
        Returns a list of strings, the strings being the off-topic names.

        If the query argument `random_items` is provided (a non-negative integer),
        then this view will return `random_items` random names from the database
        instead of returning all items at once.

        API key must be provided as header.
        """

        names = [
            entry['name'] for entry in self.db.get_all(self.table_name)
        ]

        if 'random_items' in request.args:
            random_count = request.args['random_items']
            if not random_count.isdigit():
                response = {'message': "`random_items` must be a valid integer"}
                return jsonify(response), 400

            samples = random.sample(names, int(random_count))
            return jsonify(samples)

        return jsonify(names)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.params)
    def post(self, data):
        """
        Add a new off-topic channel name to the database.
        Expects the new channel's name as the `name` argument.
        The name must consist only of alphanumeric characters or minus signs,
        and must not be empty or exceed 96 characters.

        Data must be provided as params.
        API key must be provided as header.
        """

        if self.db.get(self.table_name, data['name']) is not None:
            response = {
                'message': "An entry with the given name already exists"
            }
            return jsonify(response), 400

        self.db.insert(
            self.table_name,
            {'name': data['name']}
        )
        return jsonify({'message': 'ok'})
