# coding=utf-8

from flask import g, jsonify, request

import rethinkdb

from pysite.base_route import APIView
from pysite.constants import ErrorCodes


class TagView(APIView):
    path = "/tag"
    name = "tag"
    table = "tag"

    def __init__(self):
        # make sure the table exists
        if not self.db.create_table(self.table, {"primary_key": "tag_name"}):
            print(f"Table {self.table} exists")

    def get(self):
        """
        Data must be provided as params,
        API key must be provided as header
        """
        query = self.db.query(self.table)
        api_key = request.headers.get("X-API-Key")
        tag_name = request.args.get("tag_name")

        if self.validate_key(api_key):
            if tag_name:
                data = self.db.run(
                    query.get(tag_name),
                    coerce=dict
                )
            else:
                data = self.db.run(
                    query.pluck("tag_name"),
                    coerce=list
                )
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify(data)

    def post(self):
        """ Data must be provided as JSON. """
        rdb = rethinkdb.table(self.table)
        indata = request.get_json()
        tag_name = indata.get("tag_name")
        tag_content = indata.get("tag_content")
        tag_category = indata.get("tag_category")
        api_key = indata.get("api_key")

        if self.validate_key(api_key):
            if tag_name and tag_content:
                rdb.insert({
                    "tag_name": tag_name,
                    "tag_content": tag_content,
                    "tag_category": tag_category
                }).run(g.db.conn)
            else:
                return self.error(ErrorCodes.missing_parameters)
        else:
            return self.error(ErrorCodes.invalid_api_key)

        return jsonify({"success": True})
