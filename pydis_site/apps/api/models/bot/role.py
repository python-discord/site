from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pydis_site.apps.api.models.mixins import ModelReprMixin


class Role(ModelReprMixin, models.Model):
    """
    A role on our Discord server.

    The comparison operators <, <=, >, >=, ==, != act the same as they do with Role-objects of the
    discord.py library, see https://discordpy.readthedocs.io/en/latest/api.html#discord.Role
    """

    id = models.BigIntegerField(
        primary_key=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Role IDs cannot be negative."
            ),
        ),
        help_text="The role ID, taken from Discord.",
        verbose_name="ID"
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
    position = models.IntegerField(
        help_text="The position of the role in the role hierarchy of the Discord Guild."
    )

    def __str__(self) -> str:
        """Returns the name of the current role, for display purposes."""
        return self.name

    def __lt__(self, other: Role) -> bool:
        """Compares the roles based on their position in the role hierarchy of the guild."""
        return self.position < other.position

    def __le__(self, other: Role) -> bool:
        """Compares the roles based on their position in the role hierarchy of the guild."""
        return self.position <= other.position

    class Meta:
        """Set role ordering from highest to lowest position."""

        ordering = ("-position",)
