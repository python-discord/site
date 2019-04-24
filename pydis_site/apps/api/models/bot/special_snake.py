from django.contrib.postgres import fields as pgfields
from django.core.validators import RegexValidator
from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class SpecialSnake(ModelReprMixin, models.Model):
    """A special snake's name, info and image from our database used by the bot's snake cog."""

    name = models.CharField(
        max_length=140,
        primary_key=True,
        help_text='A special snake name.',
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )
    info = models.TextField(
        help_text='Info about a special snake.'
    )
    images = pgfields.ArrayField(
        models.URLField(),
        help_text='Images displaying this special snake.'
    )

    def __str__(self):
        """Returns the name of the current snake, for display purposes."""

        return self.name
