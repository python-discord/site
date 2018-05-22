from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin


GET_SCHEMA = Schema([
    {
        Optional("package"): str
    }
])

POST_SCHEMA = Schema([
    {
        "package": str,
        "base_url": str,
        "inventory_url": str
    }
])

DELETE_SCHEMA = Schema([
    {
        "package": str
    }
])


class DocView(APIView, DBMixin):
    path = "/bot/docs"
    name = "bot.docs"
    table_name = "pydoc_links"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        """
        Fetches documentation metadata from the database.

        - If `package` parameters are provided, fetch metadata
        for the given packages, or `[]` if none matched.

        - If `package` is not provided, return all
        packages known to the database.

        Data must be provided as params.
        API key must be provided as header.
        """

        if params:
            packages = (param['package'] for param in params if 'package' in param)
            data = self.db.get_all(self.table_name, *packages, index='package') or []
        else:
            data = self.db.pluck(self.table_name, ("package", "base_url", "inventory_url")) or []

        return jsonify(data)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, json_data):
        """
        Adds one or more new documentation metadata objects.

        If the `package` passed in the data
        already exists, it will be updated instead.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        packages_to_insert = (
            {
                "package": json_object["package"],
                "base_url": json_object["base_url"],
                "inventory_url": json_object["inventory_url"]
            } for json_object in json_data
        )

        self.db.insert(self.table_name, *packages_to_insert, conflict="update")
        return jsonify({"success": True})

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, json_data):
        """
        Deletes a documentation metadata object.
        Expects the `package` to be deleted to
        be specified as a request parameter.

        Data must be provided as params.
        API key must be provided as header.
        """

        packages = (json_object["package"]for json_object in json_data)
        changes = self.db.delete(self.table_name, *packages, return_changes=True)
        return jsonify(changes)
