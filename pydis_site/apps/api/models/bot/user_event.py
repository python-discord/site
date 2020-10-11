from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class UserEvent(ModelReprMixin, models.Model):
    """A user event in the server."""

    name = models.CharField(
        max_length=128,
        verbose_name="Event Name",
        help_text="Name of the user event.",
        unique=True
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    description = models.TextField(
        blank=True
    )
    subscriptions = models.ManyToManyField(
        User,
        blank=True,
        related_name="subscriptions"
    )
