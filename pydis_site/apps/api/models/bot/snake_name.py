from django.core.validators import RegexValidator
from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class SnakeName(ModelReprMixin, models.Model):
    """A snake name used by the bot's snake cog."""

    name = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="The regular name for this snake, e.g. 'Python'.",
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )
    scientific = models.CharField(
        max_length=150,
        help_text="The scientific name for this snake, e.g. 'Python bivittatus'.",
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )

    def __str__(self):
        """Returns the regular and scientific name of the current snake, for display purposes."""

        return f"{self.name} ({self.scientific})"
