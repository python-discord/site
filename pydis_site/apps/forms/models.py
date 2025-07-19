from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Admin(models.Model):
    """Represents an administrator of the forms backend."""

    id: models.BigIntegerField(
        primary_key=True,
        validators=(MinValueValidator(limit_value=0, message="Admin IDs can not be negative."),),
        help_text="The user ID of this administrator.",
        verbose_name="ID",
    )


# XXX: This duplicates the role object from the API app. The role object in the
# API app carries less data. We should unify these.
class DiscordRole(models.Model):
    """Represents a role as returned by the Discord API."""

    id: models.BigIntegerField(
        primary_key=True,
        validators=(MinValueValidator(limit_value=0, message="Role IDs can not be negative."),),
        help_text="The ID of this role.",
        verbose_name="ID",
    )
    name = models.CharField(max_length=100, help_text="The role name, taken from Discord.")
    colour = models.IntegerField(
        validators=(MinValueValidator(limit_value=0, message="Colour hex cannot be negative."),),
        help_text="The integer value of the colour of this role from Discord.",
    )
    hoist = models.BooleanField(help_text="Whether this role is hoisted.")
    icon = models.CharField(
        max_length=250,
        help_text="Icon hash of the role.",
        null=True,
    )
    unicode_emoji = models.CharField(
        max_length=250,
        help_text="Unicode emoji of the role.",
        null=True,
    )
    position = models.IntegerField(help_text="The position of the role in the role hierarchy of the Discord Guild.")
    permissions = models.BigIntegerField(
        validators=(MinValueValidator(limit_value=0, message="Role permissions cannot be negative."),),
        help_text="The integer value of the permission bitset of this role from Discord.",
    )
    managed = models.BooleanField(help_text="Whether this role is managed by an integration.")
    mentionable = models.BooleanField(help_text="Whether this role is mentionable.")
    role_tags = models.JSONField(
        help_text="Further metadata about this role.",
        null=True,
    )
    last_update = models.DateTimeField(
        help_text="When this role was most recently refreshed from Discord.",
        auto_now=True,
    )


# XXX: We should try to get rid of this.
class DiscordUser(models.Model):
    """Represents a user as returned by the Discord API."""

    id = models.BigIntegerField(
        primary_key=True,
        validators=(MinValueValidator(limit_value=0, message="User IDs can not be negative."),),
        help_text="The ID of this user.",
        verbose_name="ID",
    )
    username = models.CharField(
        help_text="The name of this user.",
        verbose_name="Username",
        max_length=32,
    )
    discriminator = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(limit_value=9999, message="Discriminators may not exceed `9999`."),),
        help_text="The discriminator of this user, taken from Discord.",
    )
    avatar = models.CharField(
        help_text="The avatar hash of this user.",
        verbose_name="Avatar hash",
        max_length=100,
        null=True,
    )
    bot = models.BooleanField(
        help_text="Whether this user is a bot.",
        verbose_name="Is bot",
        null=True,
    )
    system = models.BooleanField(
        help_text="Whether this user is a system user.",
        verbose_name="Is system user",
        null=True,
    )
    locale = models.CharField(
        help_text="The identifier of the locale that this user is using.",
        verbose_name="Locale identifier",
        null=True,
    )
    verified = models.BooleanField(
        help_text="Whether this user's email address is verified.",
        verbose_name="Verified email address",
        null=True,
    )
    email = models.CharField(
        help_text="The e-mail address of this user.",
        verbose_name="E-mail address",
        null=True,
    )
    flags = models.IntegerField(
        help_text="User account flags as a bitfield.",
        verbose_name="Flags",
        null=True,
    )
    premium_type = models.IntegerField(
        help_text="The type of nitro subscription on a user's account.",
        verbose_name="Nitro type",
        null=True,
    )
    public_flags = models.IntegerField(
        help_text="The public flags on a user's account.",
        verbose_name="Flags",
        null=True,
    )


# XXX: This duplicates the member object from the API app. The member object in
# the API app carries less data. We should unify these, although admittedly
# this one has the extra use of being able to filter members that use the forms
# backend, and extra data.
class DiscordMember(models.Model):
    """Represents a guild member as returned by the Discord API."""

    user = models.OneToOneField(
        DiscordUser,
        help_text="The user associated with this member.",
        on_delete=models.CASCADE,
    )
    nick = models.CharField(
        max_length=100,
        help_text="The nickname that the member is using.",
        null=True,
    )
    avatar = models.CharField(
        help_text="The avatar hash of this member for this server.",
        verbose_name="Avatar hash",
        max_length=100,
        null=True,
    )
    roles = ArrayField(
        models.BigIntegerField(
            validators=(MinValueValidator(limit_value=0, message="Role IDs cannot be negative."),),
            help_text="The snowflake ID of a role this member is part of.",
        ),
        help_text="Roles this member is part of.",
        verbose_name="Roles",
    )
    joined_at = models.DateTimeField(
        help_text="When this member has joined the guild.",
        verbose_name="Join date",
    )
    premium_since = models.DateTimeField(
        help_text="When this member started boosting the guild.",
        verbose_name="Boosting since",
        null=True,
    )
    # XXX: These should probably be removed.
    deaf = models.BooleanField(
        help_text="Whether this user is deaf.",
        verbose_name="Deaf",
    )
    mute = models.BooleanField(
        help_text="Whether this user is mute.",
        verbose_name="Mute",
    )
    pending = models.BooleanField(
        help_text="Whether this user has not yet passed membership screening.",
        verbose_name="Pending screening",
        null=True,
    )
    # XXX: This should probably be removed, seems only relevant to interactions.
    permissions = models.BigIntegerField(
        help_text="Total permissions of the member in the channel.",
        verbose_name="Pending screening",
        null=True,
    )
    communication_disabled_until = models.DateTimeField(
        help_text="Until when the user is server-muted.",
        verbose_name="Timeout until",
        null=True,
    )
    last_update = models.DateTimeField(
        help_text="When this member was most recently refreshed from Discord.",
        auto_now=True,
    )
