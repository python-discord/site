from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


class DocumentationLink(ModelReprMixin, models.Model):
    """A documentation link used by the `!docs` command of the bot."""

    package = models.CharField(
        primary_key=True,
        max_length=50,
        help_text="The Python package name that this documentation link belongs to."
    )
    base_url = models.URLField(
        help_text=(
            "The base URL from which documentation will be available for this project. "
            "Used to generate links to various symbols within this package."
        )
    )
    inventory_url = models.URLField(
        help_text="The URL at which the Sphinx inventory is available for this package."
    )

    def __str__(self):
        """Returns the package and URL for the current documentation link, for display purposes."""
        return f"{self.package} - {self.base_url}"

    class Meta:
        """Defines the meta options for the documentation link model."""

        ordering = ['package']
