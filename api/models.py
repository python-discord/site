from operator import itemgetter

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class ModelReprMixin:
    """
    Adds a `__repr__` method to the model subclassing this
    mixin which will display the model's class name along
    with all parameters used to construct the object.
    """

    def __repr__(self):
        attributes = ' '.join(
            f'{attribute}={value!r}'
            for attribute, value in sorted(
                self.__dict__.items(),
                key=itemgetter(0)
            )
            if not attribute.startswith('_')
        )
        return f'<{self.__class__.__name__}({attributes})>'


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


class OffTopicChannelName(ModelReprMixin, models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=96,
        validators=(RegexValidator(regex=r'^[a-z0-9-]+$'),),
        help_text="The actual channel name that will be used on our Discord server."
    )


class SnakeName(ModelReprMixin, models.Model):
    """A snake name used by the bot's snake cog."""

    name = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="The regular name for this snake, e.g. 'Python'."
    )
    scientific = models.CharField(
        max_length=150,
        help_text="The scientific name for this snake, e.g. 'Python bivittatus'."
    )


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


class Member(ModelReprMixin, models.Model):
    """A member of our Discord server."""

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
