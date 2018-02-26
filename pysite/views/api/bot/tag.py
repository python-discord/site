# coding=utf-8

from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ErrorCodes
from pysite.decorators import api_key
from pysite.mixins import DBMixin


class DocsView(APIView, DBMixin):
    path = "/docs"
    name = "docs"
    table_name = "docs"
    table_primary_key = "doc_name"

    @api_key
    def get(self):
        """
        Fetches docs from the database.
        - If doc_name is provided, it fetches
        that specific doc.
        - If doc_category is provided, it fetches
        all docs in that category.
        - If nothing is provided, it will
        fetch a list of all doc_names.

        Data must be provided as params.
        API key must be provided as header.
        """

        doc_name = request.args.get("doc_name")

        if doc_name:
            data = self.db.get(self.table_name, doc_name) or {}
        else:
            data = self.db.pluck(self.table_name, "doc_name") or []

        return jsonify(data)

    @api_key
    def post(self):
        """
        If the doc_name doesn't exist, this
        saves a new doc in the database.

        If the doc_name already exists,
        this will edit the existing doc.

        Data must be provided as JSON.
        API key must be provided as header.

        """

        data = request.get_json()

        doc_name = data.get("doc_name")
        doc_content = data.get("doc_content")

        if doc_name and doc_content:
            self.db.insert(
                self.table_name,
                {
                    "doc_name": doc_name,
                    "doc_content": doc_content
                },
                conflict="update"  # if it exists, update it.
            )
        else:
            return self.error(ErrorCodes.incorrect_parameters)

        return jsonify({"success": True})

    @api_key
    def delete(self):
        """
        Deletes a doc from the database.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        data = request.get_json()
        doc_name = data.get("doc_name")

        if doc_name:
            changes = self.db.delete(
                self.table_name,
                doc_name,
                return_changes=True
            )

            if changes['deleted'] != 1:
                return self.error(ErrorCodes.database_error,
                                  "Database deleted too many or too few records.")
        else:
            return self.error(ErrorCodes.incorrect_parameters)

        return jsonify({"success": True})
