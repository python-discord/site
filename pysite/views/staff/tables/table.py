from math import ceil

from flask import request
from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import TABLE_MANAGER_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin
from pysite.tables import TABLES


class TableView(RouteView, DBMixin):
    path = "/tables/<table>/<page>"
    name = "tables.table"

    @require_roles(*TABLE_MANAGER_ROLES)
    def get(self, table, page):
        search = request.args.get("search")

        pages = page
        obj = TABLES.get(table)

        if not obj:
            return NotFound()

        if search:
            new_search = f"(?i){search}"  # Case-insensitive search
            query = self.db.query(table).filter(lambda d: d[obj.primary_key].match(new_search))
        else:
            query = self.db.query(table)

        if page != "all":
            try:
                page = int(page)
            except ValueError:
                # Not an integer
                return BadRequest()

            count = self.db.run(query.count(), coerce=int)
            pages = max(ceil(count / 10), 1)  # Pages if we have 10 documents per page, always at least one

            if page < 1 or page > pages:
                # If the page is too small or too big, well, that's an error
                return BadRequest()

            documents = self.db.run(  # Get only the documents for this page
                query.skip((page - 1) * 10).limit(10),
                coerce=list
            )
        else:
            documents = self.db.run(query, coerce=list)

        documents = [dict(sorted(d.items())) for d in documents]

        return self.render(
            "staff/tables/table.html",
            table=table, documents=documents, table_obj=obj,
            page=page, pages=pages, search=search
        )
