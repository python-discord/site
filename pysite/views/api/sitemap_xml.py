from flask import Response

from pysite.base_route import RouteView


class SitemapXML(RouteView):
    path = "/sitemap.xml"
    name = "sitemap_xml"

    def get(self):
        return Response(self.render("sitemap.xml", urls=[]), content_type="application/xml")
