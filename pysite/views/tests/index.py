from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_params

LIST_SCHEMA = Schema([{"test": str}])
DICT_SCHEMA = Schema({"segfault": str})


class TestParamsView(APIView):
    path = "/testparams"
    name = "testparams"

    @api_params(schema=DICT_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, data):
        return jsonify(data)

    @api_params(schema=LIST_SCHEMA, validation_type=ValidationTypes.params)
    def post(self, data):
        jsonified = jsonify(data)
        return jsonified
