import json
from logging import getLogger

from pysite.base_route import RouteView

ICON_STYLES = {
    "branding": "fab",
    "regular": "far",
    "solid": "fas",
    "light": "fal"
}

logger = getLogger("Resources")

try:
    with open("static/resources.json") as fh:
        categories = json.load(fh)

        for category, items in categories.items():
            to_remove = []

            for name, resource in items["resources"].items():
                for url_obj in resource["urls"]:
                    icon = url_obj["icon"].lower()

                    if "/" not in icon:
                        to_remove.append(name)
                        logger.error(
                            f"Resource {name} in category {category} has an invalid icon. Icons should be of the"
                            f"form `style/name`."
                        )
                        continue

                    style, icon_name = icon.split("/")

                    if style not in ICON_STYLES:
                        to_remove.append(name)
                        logger.error(
                            f"Resource {name} in category {category} has an invalid icon style. Icon style must "
                            f"be one of {', '.join(ICON_STYLES.keys())}."
                        )
                        continue

                    url_obj["classes"] = f"{ICON_STYLES[style]} fa-{icon_name}"

            for name in to_remove:
                del items["resources"][name]
except Exception:
    getLogger("Resources").exception("Failed to load resources.json")
    categories = None


class ResourcesView(RouteView):
    path = "/info/resources"
    name = "info.resources"

    def get(self):
        return self.render("main/info/resources.html", categories=categories)
