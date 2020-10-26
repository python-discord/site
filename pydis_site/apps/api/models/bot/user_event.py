from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin


class UserEvent(ModelReprMixin, models.Model):
    """A user event in the server."""

    name = models.CharField(
        max_length=64,
        verbose_name="Event Name",
        help_text="Name of the user event.",
        primary_key=True
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The event organizer."
    )
    description = models.TextField()
    message_id = models.BigIntegerField(
        help_text=(
            "The message ID of the message "
            "sent in user events channel."
        ),
        unique=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message="message IDs cannot be negative."
            ),
        )
    )
    subscriptions = models.ManyToManyField(
        User,
        blank=True,
        related_name="subscriptions"
    )
