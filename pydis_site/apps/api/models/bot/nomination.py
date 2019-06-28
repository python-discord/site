from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.utils import ModelReprMixin


class Nomination(ModelReprMixin, models.Model):
    """A helper nomination created by staff."""

    active = models.BooleanField(
        default=True,
        help_text="Whether this nomination is still relevant."
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The staff member that nominated this user.",
        related_name='nomination_set'
    )
    reason = models.TextField(
        help_text="Why this user was nominated."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The nominated user.",
        related_name='nomination'
    )
    inserted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The creation date of this nomination."
    )
    end_reason = models.TextField(
        help_text="Why the nomination was ended.",
        default=""
    )
    ended_at = models.DateTimeField(
        auto_now_add=False,
        help_text="When the nomination was ended.",
        null=True
    )
