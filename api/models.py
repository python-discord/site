from operator import itemgetter

from django.contrib.postgres import fields as pgfields
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from .validators import validate_tag_embed


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
