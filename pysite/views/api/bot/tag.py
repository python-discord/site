# coding=utf-8

from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ErrorCodes
from pysite.decorators import api_key
from pysite.mixins import DBMixin


class TagView(APIView, DBMixin):
    path = "/tag"
    name = "tag"
    table_name = "tag"
    table_primary_key = "tag_name"

    @api_key
    def get(self):
        """
        Data must be provided as params,
        API key must be provided as header
        """

        tag_name = request.args.get("tag_name")

        if tag_name:
            data = self.db.get(self.table_name, tag_name) or {}  # pragma: no cover
        else:
            data = self.db.pluck(self.table_name, "tag_name") or []

        return jsonify(data)  # pragma: no cover

    @api_key
    def post(self):
        """
        Data must be provided as JSON.
        """

        data = request.get_json()

        tag_name = data.get("tag_name")
        tag_content = data.get("tag_content")
        tag_category = data.get("tag_category")

        if tag_name and tag_content:
            self.db.insert(
                self.table_name,
                {
                    "tag_name": tag_name,
                    "tag_content": tag_content,
                    "tag_category": tag_category
                }
            )
        else:
            return self.error(ErrorCodes.incorrect_parameters)

        return jsonify({"success": True})  # pragma: no cover
