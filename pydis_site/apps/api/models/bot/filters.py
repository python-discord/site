from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

# Must be imported that way to avoid circular imports
from .infraction import Infraction
from pydis_site.apps.api.models.mixins import ModelTimestampMixin, ModelReprMixin


class FilterListType(models.IntegerChoices):
    """Choice between allow or deny for a list type."""

    ALLOW = 1
    DENY = 0


class FilterList(ModelTimestampMixin, ModelReprMixin, models.Model):
    """Represent a list in its allow or deny form."""

    name = models.CharField(max_length=50, help_text="The unique name of this list.")
    list_type = models.IntegerField(
        choices=FilterListType.choices,
        help_text="Whether this list is an allowlist or denylist"
    )
    dm_content = models.CharField(
        max_length=1000,
        null=False,
        blank=True,
        help_text="The DM to send to a user triggering this filter."
    )
    dm_embed = models.CharField(
        max_length=2000,
        help_text="The content of the DM embed",
        null=False,
        blank=True
    )
    infraction_type = models.CharField(
        choices=[
            (choices[0].upper(), choices[1])
            for choices in [("NONE", "None"), *Infraction.TYPE_CHOICES]
        ],
        max_length=10,
        null=False,
        help_text="The infraction to apply to this user."
    )
    infraction_reason = models.CharField(
        max_length=1000,
        help_text="The reason to give for the infraction.",
        blank=True,
        null=False
    )
    infraction_duration = models.DurationField(
        null=False,
        help_text="The duration of the infraction. Null if permanent."
    )
    infraction_channel = models.BigIntegerField(
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        ),
        help_text="Channel in which to send the infraction.",
        null=False
    )
    guild_pings = ArrayField(
        models.CharField(max_length=100),
        help_text="Who to ping when this filter triggers.",
        null=False
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.", null=False)
    dm_pings = ArrayField(
        models.CharField(max_length=100),
        help_text="Who to ping when this filter triggers on a DM.",
        null=False
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it.",
        null=False
    )
    bypass_roles = ArrayField(
        models.CharField(max_length=100),
        help_text="Roles and users who can bypass this filter.",
        null=False
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled.",
        null=False
    )
    send_alert = models.BooleanField(
        help_text="Whether an alert should be sent.",
    )
    # Where a filter should apply.
    enabled_channels = ArrayField(
        models.CharField(max_length=100),
        help_text="Channels in which to run the filter even if it's disabled in the category."
    )
    disabled_channels = ArrayField(
        models.CharField(max_length=100),
        help_text="Channels in which to not run the filter."
    )
    enabled_categories = ArrayField(
        models.CharField(max_length=100),
        help_text="The only categories in which to run the filter."
    )
    disabled_categories = ArrayField(
        models.CharField(max_length=100),
        help_text="Categories in which to not run the filter."
    )

    class Meta:
        """Constrain name and list_type unique."""

        constraints = (
            UniqueConstraint(fields=("name", "list_type"), name="unique_name_type"),
        )

    def __str__(self) -> str:
        return f"Filter {FilterListType(self.list_type).label}list {self.name!r}"


class FilterBase(ModelTimestampMixin, ModelReprMixin, models.Model):
    """One specific trigger of a list."""

    content = models.CharField(max_length=100, help_text="The definition of this filter.")
    description = models.CharField(
        max_length=200,
        help_text="Why this filter has been added.", null=True
    )
    additional_field = models.JSONField(null=True, help_text="Implementation specific field.")
    filter_list = models.ForeignKey(
        FilterList, models.CASCADE, related_name="filters",
        help_text="The filter list containing this filter."
    )
    dm_content = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="The DM to send to a user triggering this filter."
    )
    dm_embed = models.CharField(
        max_length=2000,
        help_text="The content of the DM embed",
        null=True,
        blank=True
    )
    infraction_type = models.CharField(
        choices=[
            (choices[0].upper(), choices[1])
            for choices in [("NONE", "None"), *Infraction.TYPE_CHOICES]
        ],
        max_length=10,
        null=True,
        help_text="The infraction to apply to this user."
    )
    infraction_reason = models.CharField(
        max_length=1000,
        help_text="The reason to give for the infraction.",
        blank=True,
        null=True
    )
    infraction_duration = models.DurationField(
        null=True,
        help_text="The duration of the infraction. Null if permanent."
    )
    infraction_channel = models.BigIntegerField(
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        ),
        help_text="Channel in which to send the infraction.",
        null=True
    )
    guild_pings = ArrayField(
        models.CharField(max_length=100),
        help_text="Who to ping when this filter triggers.",
        null=True
    )
    filter_dm = models.BooleanField(help_text="Whether DMs should be filtered.", null=True)
    dm_pings = ArrayField(
        models.CharField(max_length=100),
        help_text="Who to ping when this filter triggers on a DM.",
        null=True
    )
    delete_messages = models.BooleanField(
        help_text="Whether this filter should delete messages triggering it.",
        null=True
    )
    bypass_roles = ArrayField(
        models.CharField(max_length=100),
        help_text="Roles and users who can bypass this filter.",
        null=True
    )
    enabled = models.BooleanField(
        help_text="Whether this filter is currently enabled.",
        null=True
    )
    send_alert = models.BooleanField(
        help_text="Whether an alert should be sent.",
        null=True
    )

    # Check FilterList model for information about these properties.
    enabled_channels = ArrayField(
        models.CharField(max_length=100),
        help_text="Channels in which to run the filter even if it's disabled in the category.",
        null=True
    )
    disabled_channels = ArrayField(
        models.CharField(max_length=100),
        help_text="Channels in which to not run the filter.", null=True
    )
    enabled_categories = ArrayField(
        models.CharField(max_length=100),
        help_text="The only categories in which to run the filter.",
        null=True
    )
    disabled_categories = ArrayField(
        models.CharField(max_length=100),
        help_text="Categories in which to not run the filter.",
        null=True
    )

    def __str__(self) -> str:
        return f"Filter {self.content!r}"

    class Meta:
        """Metaclass for FilterBase to make it abstract model."""

        abstract = True


class Filter(FilterBase):
    """
    The main Filter models based on `FilterBase`.

    The purpose to have this model is to have access to the Fields of the Filter model
    and set the unique constraint based on those fields.
    """

    class Meta:
        """Metaclass Filter to set the unique constraint."""

        constraints = (
            UniqueConstraint(
                fields=tuple(
                    [field.name for field in FilterBase._meta.fields
                     if field.name not in ("id", "description", "created_at", "updated_at")]
                ),
                name="unique_filters"),
        )
