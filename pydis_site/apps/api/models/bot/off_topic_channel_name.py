from django.core.validators import RegexValidator
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


class OffTopicChannelName(ModelReprMixin, models.Model):
    """An off-topic channel name, used during the daily channel name shuffle."""

    name = models.CharField(
        primary_key=True,
        max_length=96,
        validators=(
            RegexValidator(regex=r"^[a-z0-9\U0001d5a0-\U0001d5b9-ǃ？’']+$"),
        ),
        help_text="The actual channel name that will be used on our Discord server."
    )

    used = models.BooleanField(
        default=False,
        help_text="Whether or not this name has already been used during this rotation",
    )

    def __str__(self):
        """Returns the current off-topic name, for display purposes."""
        return self.name
