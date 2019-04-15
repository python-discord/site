from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pydis_site.apps.api.models.utils import ModelReprMixin


class Role(ModelReprMixin, models.Model):
    """A role on our Discord server."""

    id = models.BigIntegerField(  # noqa
        primary_key=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Role IDs cannot be negative."
            ),
        ),
        help_text="The role ID, taken from Discord."
    )
    name = models.CharField(
        max_length=100,
        help_text="The role name, taken from Discord."
    )
    colour = models.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Colour hex cannot be negative."
            ),
        ),
        help_text="The integer value of the colour of this role from Discord."
    )
    permissions = models.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Role permissions cannot be negative."
            ),
            MaxValueValidator(
                limit_value=2 << 32,
                message="Role permission bitset exceeds value of having all permissions"
            )
        ),
        help_text="The integer value of the permission bitset of this role from Discord."
    )

    def __str__(self):
        return self.name
