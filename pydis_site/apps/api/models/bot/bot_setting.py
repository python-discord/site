from django.contrib.postgres import fields as pgfields
from django.core.exceptions import ValidationError
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


def validate_bot_setting_name(name: str) -> None:
    """Raises a ValidationError if the given name is not a known setting."""
    known_settings = (
        'defcon',
        'news',
    )

    if name not in known_settings:
        raise ValidationError(f"`{name}` is not a known setting name.")


class BotSetting(ModelReprMixin, models.Model):
    """A configuration entry for the bot."""

    name = models.CharField(
        primary_key=True,
        max_length=50,
        validators=(validate_bot_setting_name,)
    )
    data = pgfields.JSONField(
        help_text="The actual settings of this setting."
    )
