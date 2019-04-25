from django.core.validators import RegexValidator
from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class OffTopicChannelName(ModelReprMixin, models.Model):
    """An off-topic channel name, used during the daily channel name shuffle."""

    name = models.CharField(
        primary_key=True,
        max_length=96,
        validators=(RegexValidator(regex=r'^[a-z0-9-]+$'),),
        help_text="The actual channel name that will be used on our Discord server."
    )

    def __str__(self):
        """Returns the current off-topic name, for display purposes."""

        return self.name
