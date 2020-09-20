from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.role import Role
from pydis_site.apps.api.models.mixins import ModelReprMixin


def _validate_existing_role(value: int) -> None:
    """Validate that a role exists when given in to the user model."""
    role = Role.objects.filter(id=value)

    if not role:
        raise ValidationError(f"Role with ID {value} does not exist")


class User(ModelReprMixin, models.Model):
    """A Discord user."""

    id = models.BigIntegerField(
        primary_key=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message="User IDs cannot be negative."
            ),
        ),
        verbose_name="ID",
        help_text="The ID of this user, taken from Discord."
    )
    name = models.CharField(
        max_length=32,
        help_text="The username, taken from Discord.",
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
    roles = ArrayField(
        models.BigIntegerField(
            validators=(
                MinValueValidator(
                    limit_value=0,
                    message="Role IDs cannot be negative."
                ),
                _validate_existing_role
            )
        ),
        default=list,
        blank=True,
        help_text="IDs of roles the user has on the server"
    )
    in_guild = models.BooleanField(
        default=True,
        help_text="Whether this user is in our server.",
        verbose_name="In Guild"
    )

    def __str__(self):
        """Returns the name and discriminator for the current user, for display purposes."""
        return f"{self.name}#{self.discriminator:04d}"

    @property
    def top_role(self) -> Role:
        """
        Attribute that returns the user's top role.

        This will fall back to the Developers role if the user does not have any roles.
        """
        roles = Role.objects.filter(id__in=self.roles)
        if not roles:
            return Role.objects.get(name="Developers")
        return max(roles)

    @property
    def username(self) -> str:
        """
        Returns the display version with name and discriminator as a standard attribute.

        For usability in read-only fields such as Django Admin.
        """
        return str(self)
