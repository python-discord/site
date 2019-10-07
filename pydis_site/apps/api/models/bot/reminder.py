from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.utils import ModelReprMixin


class Reminder(ModelReprMixin, models.Model):
    """A reminder created by a user."""

    active = models.BooleanField(
        default=True,
        help_text=(
            "Whether this reminder is still active. "
            "If not, it has been sent out to the user."
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The creator of this reminder."
    )
    channel_id = models.BigIntegerField(
        help_text=(
            "The channel ID that this message was "
            "sent in, taken from Discord."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        )
    )
    jump_url = models.CharFiels(
        help_text=("The jump url of the message "
                   "that created the reminder"
                  )
    )
    content = models.CharField(
        max_length=1500,
        help_text="The content that the user wants to be reminded of."
    )
    expiration = models.DateTimeField(
        help_text="When this reminder should be sent."
    )

    def __str__(self):
        """Returns some info on the current reminder, for display purposes."""
        return f"{self.content} on {self.expiration} by {self.author}"
