# coding=utf-8
from docutils.core import publish_parts
from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import ALL_STAFF_ROLES, ValidationTypes
from pysite.decorators import csrf, require_roles, api_params

SCHEMA = Schema([{
    "data": str
}])


class RenderView(APIView):
    path = "/render"  # "path" means that it accepts slashes
    name = "render"

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        if not len(data):
            return jsonify({"error": "No data!"})

        data = data[0]["data"]
        try:
            html = publish_parts(
                source=data, writer_name="html5", settings_overrides={"traceback": True, "halt_level": 2}
            )["html_body"]

            return jsonify({"data": html})
        except Exception as e:
            return jsonify({"error": str(e)})
