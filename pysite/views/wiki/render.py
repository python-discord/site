# coding=utf-8
import re

from docutils.utils import SystemMessage
from flask import jsonify
from schema import Schema

from pysite.base_route import APIView
from pysite.constants import EDITOR_ROLES, ValidationTypes
from pysite.decorators import api_params, csrf, require_roles
from pysite.rst import render

SCHEMA = Schema([{
    "data": str
}])

MESSAGE_REGEX = re.compile(r"<string>:(\d+): \([A-Z]+/\d\) (.*)")


class RenderView(APIView):
    path = "/render"  # "path" means that it accepts slashes
    name = "render"

    @csrf
    @require_roles(*EDITOR_ROLES)
    @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
    def post(self, data):
        if not len(data):
            return jsonify({"error": "No data!"})

        data = data[0]["data"]
        try:
            html = render(data)

            return jsonify({"data": html})
        except SystemMessage as e:
            lines = str(e)
            data = {
                "error": lines,
                "error_lines": []
            }

            if "\n" in lines:
                lines = lines.split("\n")
            else:
                lines = [lines]

            for message in lines:
                match = MESSAGE_REGEX.match(message)

                if match:
                    data["error_lines"].append(
                        {
                            "row": int(match.group(1)) - 1,
                            "column": 0,
                            "type": "error",
                            "text": match.group(2)
                        }
                    )

            print(data)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})
