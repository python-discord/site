from tests import SiteTest

class DecoratorTests(SiteTest):
    def test_decorator_api_json(self):
        """ Check the json validation decorator """
        from pysite.decorators import api_params
        from pysite.constants import ValidationTypes
        from schema import Schema

        SCHEMA = Schema([{"user_id": int, "role": int}])

        @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
        def try_json_type(data):
            return data

        try:
            try_json_type("not json")
        except Exception as error_message:
            self.assertEqual(type(error_message), AttributeError)

    def test_decorator_params(self):
        """ Check the params validation decorator """

        response = self.client.post('/testparams?test=params')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'test': 'params'}])
