from math import ceil

from werkzeug.exceptions import BadRequest, NotFound

from pysite.base_route import RouteView
from pysite.constants import TABLE_MANAGER_ROLES
from pysite.database import ALL_TABLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin


class TableView(RouteView, DBMixin):
    path = "/tables/<table>/<int:page>"
    name = "tables.table"

    @require_roles(*TABLE_MANAGER_ROLES)
    def get(self, table, page):
        if table not in ALL_TABLES:
            raise NotFound()

        count = self.db.run(self.db.query(table).count(), coerce=int)  # All documents in table
        pages = max(ceil(count / 10), 1)  # Pages if we have 10 documents per page, always at least one

        if page < 1 or page > pages:
            # If the page is too small or too big, well, that's an error
            return BadRequest()

        documents = self.db.run(  # Get only the documents for this page
            self.db.query(table)
                .skip((page - 1) * 10)
                .limit(page * 10),
            coerce=list
        )

        return self.render(
            "staff/tables/table.html",
            table=table, documents=documents, primary_key=ALL_TABLES[table],
            page=page, pages=pages
        )
