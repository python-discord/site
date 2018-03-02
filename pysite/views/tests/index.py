# coding=utf-8

from flask import jsonify

from pysite.base_route import RouteView
from pysite.constants import ValidationTypes
from pysite.decorators import api_params

from schema import Schema

SCHEMA = Schema([{"test": str}])

REQUIRED_KEYS = ["test"]


class TestParamsView(RouteView):
    path = "/testparams"
    name = "testparams"

    @api_params(schema=SCHEMA, validation_type=ValidationTypes.params)
    def post(self, data):
        jsonified = jsonify(data)
        return jsonified
