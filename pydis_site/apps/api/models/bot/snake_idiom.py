from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class SnakeIdiom(ModelReprMixin, models.Model):
    """A snake idiom used by the snake cog."""

    idiom = models.CharField(
        primary_key=True,
        max_length=140,
        help_text="A saying about a snake."
    )

    def __str__(self):
        """Returns the current idiom, for display purposes."""

        return self.idiom
