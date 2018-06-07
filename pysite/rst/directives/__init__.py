import pprint

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged, unchanged_required
from flask import url_for
from jinja2 import escape

BUTTON_TYPES = ("default", "primary", "secondary", "danger", "darkish", "darker")

ICON_WEIGHT_TABLE = {
    "light": "fal",
    "regular": "far",
    "solid": "fas",
    "branding": "fab"
}
ICON_WEIGHTS = tuple(ICON_WEIGHT_TABLE.values())


class ButtonDirective(Directive):
    has_content = True

    option_spec = {
        "icon": unchanged_required,
        "text": unchanged_required,
        "type": unchanged,
        "url": unchanged,
    }

    def run(self):
        pprint.pprint(self.__dict__)  # DEBUG

        icon = self.options.get("icon", "")
        button_type = self.options.get("type", "primary")

        text = self.options["text"]
        url = self.options["url"]

        if icon:
            parts = [escape(x) for x in icon.split("/")]

            if len(parts) != 2:
                raise self.error("Icon specification must be in the form <type>/<name>")
            elif parts:
                weight = parts[0]

                if weight not in ICON_WEIGHTS:
                    weight = ICON_WEIGHT_TABLE.get(weight)

                    if not weight:
                        raise self.error(
                            "Icon type must be one of light, regular, solid or "
                            "branding, or a font-awesome weight class"
                        )

                icon_html = f"""<i class="uk-icon fa-fw {weight} fa-{parts[1]}"></i>"""
        else:
            icon_html = ""

        if button_type not in BUTTON_TYPES:
            self.error(f"Button type must be one of {', '.join(BUTTON_TYPES[:-1])} or {[-1]}")

        if url.startswith("flask://"):
            url = url_for(url.split("://", 1)[1])
        elif url.startswith("wiki://"):
            url = url_for("wiki.page", page=url.split("://", 1)[1])
        html = f"""<a class="uk-button uk-button-{button_type}" href=\"{url}\">{icon_html} &nbsp;{text}</a>"""

        return [nodes.raw(html, html, format="html", **{})]
