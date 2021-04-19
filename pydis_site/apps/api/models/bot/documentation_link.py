from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin

package_name_validator = RegexValidator(
    regex=r"^[a-z0-9_]+$",
    message="Package names can only consist of lowercase a-z letters, digits, and underscores."
)


def ends_with_slash_validator(string: str) -> None:
    """Raise a ValidationError if `string` does not end with a slash."""
    if not string.endswith("/"):
        raise ValidationError("The entered URL must end with a slash.")


class DocumentationLink(ModelReprMixin, models.Model):
    """A documentation link used by the `!docs` command of the bot."""

    package = models.CharField(
        primary_key=True,
        max_length=50,
        validators=(package_name_validator,),
        help_text="The Python package name that this documentation link belongs to."
    )
    base_url = models.URLField(
        help_text=(
            "The base URL from which documentation will be available for this project. "
            "Used to generate links to various symbols within this package."
        ),
        validators=(ends_with_slash_validator,)
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
