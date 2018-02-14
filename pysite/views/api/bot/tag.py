# coding=utf-8

from flask import jsonify, request

from pysite.base_route import APIView, DBViewMixin
from pysite.constants import ErrorCodes


class TagView(APIView, DBViewMixin):
    path = "/tag"
    name = "tag"
    table_name = "tag"
    table_primary_key = "tag_name"

    def get(self):
        """
        Data must be provided as params,
        API key must be provided as header
        """
        api_key = request.headers.get("X-API-Key")
        tag_name = request.args.get("tag_name")

        if self.validate_key(api_key):
            if tag_name:
                data = self.db.get(self.table_name, tag_name)
            else:
                data = self.db.pluck(self.table_name, "tag_name")
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify(data if data is not None else {})

    def post(self):
        """ Data must be provided as JSON. """
        indata = request.get_json()
        tag_name = indata.get("tag_name")
        tag_content = indata.get("tag_content")
        tag_category = indata.get("tag_category")
        api_key = indata.get("api_key")

        if self.validate_key(api_key):
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
                return self.error(ErrorCodes.missing_parameters)
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify({"success": True})
