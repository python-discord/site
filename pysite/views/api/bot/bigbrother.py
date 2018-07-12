import json

from flask import jsonify
from schema import And, Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin


GET_SCHEMA = Schema({
    # This is passed as a GET parameter, so it has to be a string
    Optional('user_id'): And(str, str.isnumeric, error="`user_id` must be a numeric string")
})

POST_SCHEMA = Schema({
    'user_id': And(str, str.isnumeric, error="`user_id` must be a numeric string"),
    'channel_id': And(str, str.isnumeric, error="`channel_id` must be a numeric string")
})

DELETE_SCHEMA = Schema({
    'user_id': And(str, str.isnumeric, error="`user_id` must be a numeric string")
})


NOT_A_NUMBER_JSON = json.dumps({
    'error_message': "The given `user_id` parameter is not a valid number"
})
NOT_FOUND_JSON = json.dumps({
    'error_message': "No entry for the requested user ID could be found."
})


class BigBrotherView(APIView, DBMixin):
    path = '/bot/bigbrother'
    name = 'bot.bigbrother'
    table_name = 'watched_users'

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params):
        """
        Without query parameters, returns a list of all monitored users.
        A parameter `user_id` can be specified to return a single entry,
        or a dictionary with the string field 'error_message' that tells why it failed.

        If the returned status is 200, has got either a list of entries
        or a single object (see above).

        If the returned status is 400, the `user_id` parameter was incorrectly specified.
        If the returned status is 404, the given `user_id` could not be found.
        See the 'error_message' field in the JSON response for more information.

        The user ID must be provided as query parameter.
        API key must be provided as header.
        """

        user_id = params.get('user_id')
        if user_id is not None:
            data = self.db.get(self.table_name, user_id)
            if data is None:
                return NOT_FOUND_JSON, 404
            return jsonify(data)

        else:
            data = self.db.pluck(self.table_name, ('user_id', 'channel_id')) or []
            return jsonify(data)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        """
        Adds a new entry to the database.
        Entries take the following form:
        {
            "user_id": ...,  # The user ID of the user being monitored, as a string.
            "channel_id": ...  # The channel ID that the user's messages will be relayed to, as a string.
        }

        If an entry for the given `user_id` already exists, it will be updated with the new channel ID.

        Returns 204 (ok, empty response) on success.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        self.db.insert(
            self.table_name,
            {
                'user_id': data['user_id'],
                'channel_id': data['channel_id']
            },
            conflict='update'
        )

        return '', 204

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.params)
    def delete(self, params):
        """
        Removes an entry for the given `user_id`.

        Returns 204 (ok, empty response) on success.
        Returns 400 if the given `user_id` is invalid.

        The user ID must be provided as query parameter.
        API key must be provided as header.
        """

        self.db.delete(
            self.table_name,
            params['user_id']
        )

        return '', 204
