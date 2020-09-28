import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


def future_date_validator(date: datetime.date) -> None:
    """Raise ValidationError if the date isn't a future date."""
    if date < datetime.datetime.now(datetime.timezone.utc):
        raise ValidationError("Date must be a future date")


class OffensiveMessage(ModelReprMixin, models.Model):
    """A message that triggered a filter and that will be deleted one week after it was sent."""

    id = models.BigIntegerField(
        primary_key=True,
        help_text="The message ID as taken from Discord.",
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Message IDs cannot be negative."
            ),
        ),
        verbose_name="Message ID"
    )
    channel_id = models.BigIntegerField(
        help_text=(
            "The channel ID that the message was "
            "sent in, taken from Discord."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        ),
        verbose_name="Channel ID"
    )
    delete_date = models.DateTimeField(
        help_text="The date on which the message will be auto-deleted.",
        validators=(future_date_validator,),
        verbose_name="To Be Deleted"
    )

    def __str__(self):
        """Return some info on this message, for display purposes only."""
        return f"Message {self.id}, will be deleted at {self.delete_date}"
