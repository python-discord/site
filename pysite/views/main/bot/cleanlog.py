import logging

from pysite.base_route import RouteView
from pysite.constants import ALL_STAFF_ROLES, DEVELOPERS_ROLE, ROLE_COLORS
from pysite.decorators import require_roles
from pysite.mixins import DBMixin, OAuthMixin

log = logging.getLogger(__name__)


class CleanLogView(RouteView, DBMixin, OAuthMixin):
    path = "/bot/clean_logs/<log_id>"
    name = "bot.clean_logs"

    table_name = "clean_logs"
    template = "main/bot/clean_logs.html"

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
            message['color'] = ROLE_COLORS.get(message['role_id'], ROLE_COLORS[DEVELOPERS_ROLE])

        return self.render(self.template, messages=messages)
