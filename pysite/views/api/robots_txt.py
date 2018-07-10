from flask import Response, url_for

from pysite.base_route import RouteView


class RobotsTXT(RouteView):
    path = "/robots.txt"
    name = "robots_txt"

    def get(self):
        return Response(
            self.render(
                "robots.txt", sitemap_url=url_for("api.sitemap_xml", _external=True), rules={"*": ["/"]}
            ), content_type="text/plain"
        )
