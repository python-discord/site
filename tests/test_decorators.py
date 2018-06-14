from schema import Schema
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import BadRequest

from pysite.constants import ValidationTypes
from pysite.decorators import api_params
from tests import SiteTest


class DuckRequest:
    """A quacking request with the `args` parameter used in schema validation."""

    def __init__(self, args):
        self.args = args


class DecoratorTests(SiteTest):
    def test_decorator_api_json(self):
        """ Check the json validation decorator """
        SCHEMA = Schema([{"user_id": int, "role": int}])

        @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
        def try_json_type(data):
            return data

        with self.assertRaises(AttributeError):
            try_json_type("not json")

    def test_decorator_params(self):
        """ Check the params validation decorator """

        response = self.client.post('/testparams?test=params')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'test': 'params'}])

    def test_duplicate_params_with_dict_schema_raises_400(self):
        """Check that duplicate parameters with a dictionary schema return 400 Bad Request"""

        response = self.client.get('/testparams?segfault=yes&segfault=no')
        self.assert400(response)

    def test_single_params_with_dict_schema(self):
        """Single parameters with a dictionary schema and `allow_duplicate_keys=False` return 200"""

        response = self.client.get('/testparams?segfault=yes')
        self.assert200(response)
        self.assertEqual(response.json, {'segfault': 'yes'})
