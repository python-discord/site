from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class AocCompletionistBlock(ModelReprMixin, models.Model):
    """A Discord user blocked from getting the AoC completionist Role."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user that is blocked from getting the AoC Completionist Role"
    )

    is_blocked = models.BooleanField(
        default=True,
        help_text="Whether this user is actively being blocked "
                  "from getting the AoC Completionist Role",
        verbose_name="Blocked"
    )
