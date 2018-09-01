from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class DocumentationLink(models.Model):
    """A documentation link used by the `!docs` command of the bot."""

    package = models.CharField(primary_key=True, max_length=50)
    base_url = models.URLField()
    inventory_url = models.URLField()


class OffTopicChannelName(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=96,
        validators=(RegexValidator(regex=r'^[a-z0-9-]+$'),)
    )


class SnakeName(models.Model):
    """A snake name used by the bot's snake cog."""

    name = models.CharField(primary_key=True, max_length=100)
    scientific = models.CharField(max_length=150)


class Role(models.Model):
    """A role on our Discord server."""

    id = models.BigIntegerField(
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


class Member(models.Model):
    """A member of our Discord server."""

    id = models.BigIntegerField(
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
