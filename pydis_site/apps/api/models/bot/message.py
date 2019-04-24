from django.contrib.postgres import fields as pgfields
from django.core.validators import MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.tag import validate_tag_embed
from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.models.utils import ModelReprMixin


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
        )
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
        )
    )
    content = models.CharField(
        max_length=2_000,
        help_text="The content of this message, taken from Discord.",
        blank=True
    )
    embeds = pgfields.ArrayField(
        pgfields.JSONField(
            validators=(validate_tag_embed,)
        ),
        help_text="Embeds attached to this message."
    )

    class Meta:
        """Metadata provided for Django's ORM."""

        abstract = True
