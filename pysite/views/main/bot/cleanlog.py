import logging
import random

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES
from pysite.decorators import require_roles
from pysite.mixins import DBMixin, OAuthMixin

log = logging.getLogger(__name__)


class CleanLogView(RouteView, DBMixin, OAuthMixin):
    path = "/bot/clean_logs/<log_id>"
    name = "bot.clean_logs"

    table_name = "clean_logs"
    template = "main/bot/clean_logs.html"

    # Colors
    author_colors = {}
    all_colors = [
        "#afcfff",
        "#93ff91",
        "#ffe559",
        "#ff9036",
        "#ff6c5e",
        "#ff65be",
        "#9298ff",
    ]
    color_pool = all_colors

    def _assign_color(self, author):
        """
        Assign a color to a specific author.
        """

        if not self.color_pool:
            self.color_pool = self.all_colors

        if author not in self.author_colors:
            random_index = random.randint(0, len(self.color_pool))
            color = self.color_pool.pop(random_index)
            self.author_colors[author] = color
            return color
        else:
            return self.author_colors[author]

    @require_roles(ALL_STAFF_ROLES)
    def get(self, log_id):
        """
        Get the requested clean log and spit it out
        in a beautiful template.
        """

        data = self.db.get(self.table_name, log_id)

        if data is None:
            return "ID could not be found in the database", 404

        messages = data["log_data"]

        for message in messages:
            message['color'] = self._assign_color(message['author'])

        return self.render(self.template, messages=messages)
