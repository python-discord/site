# coding=utf-8

from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ErrorCodes
from pysite.decorators import api_key
from pysite.mixins import DBMixin


class TagsView(APIView, DBMixin):
    path = "/tags"
    name = "tags"
    table_name = "tags"
    table_primary_key = "tag_name"

    @api_key
    def get(self):
        """
        Fetches tags from the database.
        - If tag_name is provided, it fetches
        that specific tag.
        - If tag_category is provided, it fetches
        all tags in that category.
        - If nothing is provided, it will
        fetch a list of all tag_names.

        Data must be provided as params.
        API key must be provided as header.
        """

        tag_name = request.args.get("tag_name")

        if tag_name:
            data = self.db.get(self.table_name, tag_name) or {}
        else:
            data = self.db.pluck(self.table_name, "tag_name") or []

        return jsonify(data)

    @api_key
    def post(self):
        """
        If the tag_name doesn't exist, this
        saves a new tag in the database.

        If the tag_name already exists,
        this will edit the existing tag.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        data = request.get_json()

        tag_name = data.get("tag_name")
        tag_content = data.get("tag_content")

        if tag_name and tag_content:
            self.db.insert(
                self.table_name,
                {
                    "tag_name": tag_name,
                    "tag_content": tag_content
                },
                conflict="update"  # If it exists, update it.
            )
        else:
            return self.error(ErrorCodes.incorrect_parameters)

        return jsonify({"success": True})

    @api_key
    def delete(self):
        """
        Deletes a tag from the database.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        data = request.get_json()
        tag_name = data.get("tag_name")

        if tag_name:
            changes = self.db.delete(
                self.table_name,
                tag_name,
                return_changes=True
            )

            if changes['deleted'] > 1:
                return self.error(
                    ErrorCodes.database_error,
                    "Database deleted more than one record. "
                    "This shouldn't be possible, please investigate. \n"
                    "The following changes were made: \n"
                    f"{changes['changes']}"
                )
        else:
            return self.error(ErrorCodes.incorrect_parameters)

        return jsonify({"success": True})
