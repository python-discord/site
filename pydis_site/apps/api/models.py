from operator import itemgetter

from django.contrib.postgres import fields as pgfields
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from .validators import validate_bot_setting_name, validate_tag_embed


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


class BotSetting(ModelReprMixin, models.Model):
    """A configuration entry for the bot."""

    name = models.CharField(
        primary_key=True,
        max_length=50,
        validators=(validate_bot_setting_name,)
    )
    data = pgfields.JSONField(
        help_text="The actual settings of this setting."
    )


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

    def __str__(self):
        return f"{self.package} - {self.base_url}"


class OffTopicChannelName(ModelReprMixin, models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=96,
        validators=(RegexValidator(regex=r'^[a-z0-9-]+$'),),
        help_text="The actual channel name that will be used on our Discord server."
    )

    def __str__(self):
        return self.name


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


class SnakeFact(ModelReprMixin, models.Model):
    """A snake fact used by the bot's snake cog."""

    fact = models.CharField(
        primary_key=True,
        max_length=200,
        help_text="A fact about snakes."
    )

    def __str__(self):
        return self.fact


class SnakeIdiom(ModelReprMixin, models.Model):
    """A snake idiom used by the snake cog."""

    idiom = models.CharField(
        primary_key=True,
        max_length=140,
        help_text="A saying about a snake."
    )

    def __str__(self):
        return self.idiom


class SnakeName(ModelReprMixin, models.Model):
    """A snake name used by the bot's snake cog."""

    name = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="The regular name for this snake, e.g. 'Python'.",
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )
    scientific = models.CharField(
        max_length=150,
        help_text="The scientific name for this snake, e.g. 'Python bivittatus'.",
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )

    def __str__(self):
        return f"{self.name} ({self.scientific})"


class SpecialSnake(ModelReprMixin, models.Model):
    """A special snake's name, info and image from our database used by the bot's snake cog."""

    name = models.CharField(
        max_length=140,
        primary_key=True,
        help_text='A special snake name.',
        validators=[RegexValidator(regex=r'^([^0-9])+$')]
    )
    info = models.TextField(
        help_text='Info about a special snake.'
    )
    images = pgfields.ArrayField(
        models.URLField(),
        help_text='Images displaying this special snake.'
    )

    def __str__(self):
        return self.name


class Tag(ModelReprMixin, models.Model):
    """A tag providing (hopefully) useful information."""

    title = models.CharField(
        max_length=100,
        help_text=(
            "The title of this tag, shown in searches and providing "
            "a quick overview over what this embed contains."
        ),
        primary_key=True
    )
    embed = pgfields.JSONField(
        help_text="The actual embed shown by this tag.",
        validators=(validate_tag_embed,)
    )

    def __str__(self):
        return self.title


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
        return f"{self.name}#{self.discriminator}"


class Message(ModelReprMixin, models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        help_text="The message ID as taken from Discord.",
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Message IDs cannot be negative."
            ),
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The author of this message."
    )
    channel_id = models.BigIntegerField(
        help_text=(
            "The channel ID that this message was "
            "sent in, taken from Discord."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        )
    )
    content = models.CharField(
        max_length=2_000,
        help_text="The content of this message, taken from Discord.",
        blank=True
    )
    embeds = pgfields.ArrayField(
        pgfields.JSONField(
            validators=(validate_tag_embed,)
        ),
        help_text="Embeds attached to this message."
    )

    class Meta:
        abstract = True


class MessageDeletionContext(ModelReprMixin, models.Model):
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=(
            "The original actor causing this deletion. Could be the author "
            "of a manual clean command invocation, the bot when executing "
            "automatic actions, or nothing to indicate that the bulk "
            "deletion was not issued by us."
        ),
        null=True
    )
    creation = models.DateTimeField(
        # Consider whether we want to add a validator here that ensures
        # the deletion context does not take place in the future.
        help_text="When this deletion took place."
    )


class DeletedMessage(Message):
    deletion_context = models.ForeignKey(
        MessageDeletionContext,
        help_text="The deletion context this message is part of.",
        on_delete=models.CASCADE
    )


class Infraction(ModelReprMixin, models.Model):
    """An infraction for a Discord user."""

    TYPE_CHOICES = (
        ("note", "Note"),
        ("warning", "Warning"),
        ("watch", "Watch"),
        ("mute", "Mute"),
        ("kick", "Kick"),
        ("ban", "Ban"),
        ("superstar", "Superstar")
    )
    inserted_at = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time of the creation of this infraction."
    )
    expires_at = models.DateTimeField(
        null=True,
        help_text=(
            "The date and time of the expiration of this infraction. "
            "Null if the infraction is permanent or it can't expire."
        )
    )
    active = models.BooleanField(
        default=True,
        help_text="Whether the infraction is still active."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='infractions_received',
        help_text="The user to which the infraction was applied."
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='infractions_given',
        help_text="The user which applied the infraction."
    )
    type = models.CharField(
        max_length=9,
        choices=TYPE_CHOICES,
        help_text="The type of the infraction."
    )
    reason = models.TextField(
        null=True,
        help_text="The reason for the infraction."
    )
    hidden = models.BooleanField(
        default=False,
        help_text="Whether the infraction is a shadow infraction."
    )

    def __str__(self):
        s = f"#{self.id}: {self.type} on {self.user_id}"
        if self.expires_at:
            s += f" until {self.expires_at}"
        if self.hidden:
            s += " (hidden)"
        return s


class Reminder(ModelReprMixin, models.Model):
    """A reminder created by a user."""

    active = models.BooleanField(
        default=True,
        help_text=(
            "Whether this reminder is still active. "
            "If not, it has been sent out to the user."
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The creator of this reminder."
    )
    channel_id = models.BigIntegerField(
        help_text=(
            "The channel ID that this message was "
            "sent in, taken from Discord."
        ),
        validators=(
            MinValueValidator(
                limit_value=0,
                message="Channel IDs cannot be negative."
            ),
        )
    )
    content = models.CharField(
        max_length=1500,
        help_text="The content that the user wants to be reminded of."
    )
    expiration = models.DateTimeField(
        help_text="When this reminder should be sent."
    )

    def __str__(self):
        return f"{self.content} on {self.expiration} by {self.author}"


class Nomination(ModelReprMixin, models.Model):
    """A helper nomination created by staff."""

    active = models.BooleanField(
        default=True,
        help_text="Whether this nomination is still relevant."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The staff member that nominated this user.",
        related_name='nomination_set'
    )
    reason = models.TextField(
        help_text="Why this user was nominated."
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="The nominated user.",
        primary_key=True,
        related_name='nomination'
    )
    inserted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The creation date of this nomination."
    )

class LogEntry(ModelReprMixin, models.Model):
    """A log entry generated by one of the PyDis applications."""

    application = models.CharField(
        max_length=20,
        help_text="The application that generated this log entry.",
        choices=(
            ('bot', 'Bot'),
            ('seasonalbot', 'Seasonalbot'),
            ('site', 'Website')
        )
    )
    logger_name = models.CharField(
        max_length=100,
        help_text="The name of the logger that generated this log entry."
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time when this entry was created."
    )
    level = models.CharField(
        max_length=8,  # 'critical'
        choices=(
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('critical', 'Critical')
        ),
        help_text=(
            "The logger level at which this entry was emitted. The levels "
            "correspond to the Python `logging` levels."
        )
    )
    module = models.CharField(
        max_length=100,
        help_text="The fully qualified path of the module generating this log line."
    )
    line = models.PositiveSmallIntegerField(
        help_text="The line at which the log line was emitted."
    )
