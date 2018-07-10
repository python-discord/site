from flask import Response, url_for

from pysite.base_route import RouteView
from pysite.mixins import DBMixin


class SitemapXML(RouteView, DBMixin):
    path = "/sitemap.xml"
    name = "sitemap_xml"
    table_name = "wiki"

    def get(self):
        urls = []

        for page in self.db.get_all(self.table_name):
            urls.append({
                "change_frequency": "weekly",
                "type": "url",
                "url": url_for("wiki.page", page=page["slug"], _external=True)
            })

        return Response(self.render("sitemap.xml", urls=urls), content_type="application/xml")
