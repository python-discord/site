import json

from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import TABLE_MANAGER_ROLES
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin
from pysite.tables import TABLES


class TableEditView(RouteView, DBMixin):
    path = "/tables/<table>/edit"
    name = "tables.edit"

    @require_roles(*TABLE_MANAGER_ROLES)
    def get(self, table):
        obj = TABLES.get(table)

        if not obj:
            # Unknown table
            raise NotFound()

        if obj.locked:
            return redirect(url_for("staff.tables.table", table=table, page=1), code=303)

        key = request.args.get("key")

        old_primary = None

        if key:
            db_obj = self.db.get(table, key)
            old_primary = key  # Provide the current document's primary key, in case it's modified

            document = json.dumps(  # Editor uses JSON
                db_obj,
                indent=4
            )
        else:
            document = json.dumps(  # Generate default document from key schema
                {k: "" for k in obj.keys},
                indent=4
            )

        return self.render(
            "staff/tables/edit.html", table=table, primary_key=obj.primary_key,
            document=document, old_primary=old_primary
        )

    @require_roles(*TABLE_MANAGER_ROLES)
    @csrf
    def post(self, table):
        obj = TABLES.get(table)

        if not obj:
            # Unknown table
            raise NotFound()

        if obj.locked:
            raise BadRequest()

        data = request.form.get("json")
        old_primary = request.form.get("old_primary")

        if not data:
            # No data given (for some reason)
            document = json.dumps(
                {k: "" for k in obj.keys},
                indent=4
            )

            return self.render(
                "staff/tables/edit.html", table=table, primary_key=obj.primary_key, document=document,
                message="Please provide some data to save", old_primary=old_primary
            )

        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            # Invalid JSON
            return self.render(
                "staff/tables/edit.html", table=table, primary_key=obj.primary_key, document=data,
                message=f"Invalid JSON, please try again: {e}", old_primary=old_primary
            )

        if not data[obj.primary_key]:
            # No primary key value provided
            return self.render(
                "staff/tables/edit.html", table=table, primary_key=obj.primary_key, document=data,
                message=f"Please provide a value for the primary key: {obj.primary_key}", old_primary=old_primary
            )

        if old_primary is None:
            self.db.insert(  # This is a new object, so just insert it
                table, data
            )
        elif old_primary == data[obj.primary_key]:
            self.db.insert(  # This is an update without a primary key change, replace the whole document
                table, data, conflict="replace"
            )
        else:
            self.db.delete(  # This is a primary key change, so we need to remove the old object
                table, old_primary
            )
            self.db.insert(
                table, data,
            )

        return redirect(url_for("staff.tables.table", table=table, page=1), code=303)
