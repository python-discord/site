from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class SnakeFact(ModelReprMixin, models.Model):
    """A snake fact used by the bot's snake cog."""

    fact = models.CharField(
        primary_key=True,
        max_length=200,
        help_text="A fact about snakes."
    )

    def __str__(self):
        return self.fact
