from datetime import datetime

from django.contrib.postgres import fields as pgfields
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.mixins import ModelReprMixin
from pydis_site.apps.api.models.utils import validate_embed


class Message(ModelReprMixin, models.Model):
    """A message, sent somewhere on the Discord server."""

    id = models.BigIntegerField(
        primary_key=True,
        help_text="The message ID as taken from Discord.",
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Message IDs cannot be negative."
            ),
        ),
        verbose_name="ID"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The author of this message."
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
        ),
        verbose_name="Channel ID"
    )
    content = models.CharField(
        max_length=2_000,
        help_text="The content of this message, taken from Discord.",
        blank=True
    )
    embeds = pgfields.ArrayField(
        pgfields.JSONField(
            validators=(validate_embed,)
        ),
        blank=True,
        help_text="Embeds attached to this message."
    )
    attachments = pgfields.ArrayField(
        models.URLField(
            max_length=512
        ),
        blank=True,
        help_text="Attachments attached to this message."
    )

    @property
    def timestamp(self) -> datetime:
        """Attribute that represents the message timestamp as derived from the snowflake id."""
        tz_naive_datetime = datetime.utcfromtimestamp(((self.id >> 22) + 1420070400000) / 1000)
        tz_aware_datetime = timezone.make_aware(tz_naive_datetime, timezone=timezone.utc)
        return tz_aware_datetime

    class Meta:
        """Metadata provided for Django's ORM."""

        abstract = True
