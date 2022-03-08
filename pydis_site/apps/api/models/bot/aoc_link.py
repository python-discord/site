from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class AocAccountLink(ModelReprMixin, models.Model):
    """An AoC account link for a Discord User."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="The user that is blocked from getting the AoC Completionist Role"
    )

    aoc_username = models.CharField(
        max_length=120,
        help_text="The AoC username associated with the Discord User.",
        blank=False
    )
