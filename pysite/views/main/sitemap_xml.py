from flask import Response, url_for

from pysite.base_route import RouteView


class SitemapXML(RouteView):
    path = "/sitemap.xml"
    name = "sitemap_xml"

    def get(self):
        urls = [
            {
                "type": "url",
                "url": url_for("main.index", _external=True),
                "priority": 1.0,  # Max priority

                "images": [
                    {
                        "caption": "Python Discord Logo",
                        "url": url_for("static", filename="logos/logo_discord.png", _external=True)
                    },
                    {
                        "caption": "Python Discord Banner",
                        "url": url_for("static", filename="logos/logo_banner.png", _external=True)
                    }
                ]
            },

            {
                "type": "url",
                "url": url_for("main.jams.index", _external=True),
                "priority": 0.9  # Above normal priority
            },

            {
                "type": "url",
                "url": url_for("main.about.privacy", _external=True),
                "priority": 0.8  # Above normal priority
            },
            {
                "type": "url",
                "url": url_for("main.about.rules", _external=True),
                "priority": 0.8  # Above normal priority
            },

            {
                "type": "url",
                "url": url_for("main.info.help", _external=True),
                "priority": 0.7  # Above normal priority
            },
            {
                "type": "url",
                "url": url_for("main.info.faq", _external=True),
                "priority": 0.7  # Above normal priority
            },
            {
                "type": "url",
                "url": url_for("main.info.resources", _external=True),
                "priority": 0.7  # Above normal priority
            },

            {
                "type": "url",
                "url": url_for("main.about.partners", _external=True),
                "priority": 0.6  # Normal priority
            },
        ]

        return Response(self.render("sitemap.xml", urls=urls), content_type="application/xml")
