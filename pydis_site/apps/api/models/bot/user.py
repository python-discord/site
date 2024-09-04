from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pydis_site.apps.api.models.bot.role import Role
from pydis_site.apps.api.models.mixins import ModelReprMixin, ModelTimestampMixin


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
    display_name = models.CharField(
        max_length=32,
        blank=True,
        help_text="The display name, taken from Discord.",
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
    alts = models.ManyToManyField(
        'self',
        through='UserAltRelationship',
        through_fields=('source', 'target'),
        help_text="Known alternate accounts of this user. Manually linked.",
        verbose_name="Alternative accounts"
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

class UserAltRelationship(ModelReprMixin, ModelTimestampMixin, models.Model):
    """A relationship between a Discord user and its alts."""

    source = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Source",
        help_text="The source of this user to alternate account relationship",
    )
    target = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Target",
        related_name='+',
        help_text="The target of this user to alternate account relationship",
    )
    context = models.TextField(
        help_text="The reason for why this account was associated as an alt.",
        max_length=1900
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        help_text="The moderator that associated these accounts together."
    )

    class Meta:
        """Add constraints to prevent users from being an alt of themselves."""

        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["source", "target"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_alt_to_self",
                condition=~models.Q(source=models.F("target")),
            ),
        ]

class UserModSettings(ModelReprMixin, models.Model):
    """Moderation settings for a Moderator member of staff."""

    moderator = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="mod_settings",
        help_text="The moderator for whom these settings belong to"
    )

    pings_disabled_until = models.DateTimeField(
        null=True,
        help_text="Date and time that moderation pings are disabled until"
    )

    pings_schedule_start = models.TimeField(
        null=True,
        help_text="UTC time that the moderator wishes to receive pings from"
    )

    pings_schedule_end = models.DurationField(
        null=True,
        help_text="Duration after the schedule start time the moderator wishes to receive pings"
    )

    class Meta:
        """Meta options on the moderator preferences."""

        constraints = [
            models.CheckConstraint(
                check=models.Q(pings_schedule_start__isnull=True, pings_schedule_end__isnull=True)
                | models.Q(pings_schedule_start__isnull=False, pings_schedule_end__isnull=False),
                name="complete_pings_schedule"
            )
        ]
