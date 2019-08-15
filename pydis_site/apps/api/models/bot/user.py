from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.role import Role
from pydis_site.apps.api.models.utils import ModelReprMixin


class User(ModelReprMixin, models.Model):
    """A Discord user."""

    id = models.BigIntegerField(  # noqa
        primary_key=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message="User IDs cannot be negative."
            ),
        ),
        help_text="The ID of this user, taken from Discord."
    )
    name = models.CharField(
        max_length=32,
        help_text="The username, taken from Discord."
    )
    discriminator = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(
                limit_value=9999,
                message="Discriminators may not exceed `9999`."
            ),
        ),
        help_text="The discriminator of this user, taken from Discord."
    )
    avatar_hash = models.CharField(
        max_length=100,
        help_text=(
            "The user's avatar hash, taken from Discord. "
            "Null if the user does not have any custom avatar."
        ),
        null=True
    )
    roles = models.ManyToManyField(
        Role,
        help_text="Any roles this user has on our server."
    )
    in_guild = models.BooleanField(
        default=True,
        help_text="Whether this user is in our server."
    )

    def __str__(self):
        """Returns the name and discriminator for the current user, for display purposes."""
        return f"{self.name}#{self.discriminator}"

    @property
    def top_role(self) -> Role:
        """Attribute that returns the user's top role."""
        return max(self.roles.all())
