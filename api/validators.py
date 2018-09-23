from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator


def validate_tag_embed_fields(fields):
    field_validators = {
        'name': (MaxLengthValidator(limit_value=256),),
        'value': (MaxLengthValidator(limit_value=1024),)
    }

    for field in fields:
        if not isinstance(field, Mapping):
            raise ValidationError("Embed fields must be a mapping.")

        for field_name, value in field.items():
            if field_name not in field_validators:
                raise ValidationError(f"Unknown embed field field: {field_name!r}.")

            for validator in field_validators[field_name]:
                validator(value)


def validate_tag_embed_footer(footer):
    field_validators = {
        'text': (
            MinLengthValidator(
                limit_value=1,
                message="Footer text must not be empty."
            ),
            MaxLengthValidator(limit_value=2048)
        ),
        'icon_url': (),
        'proxy_icon_url': ()
    }

    if not isinstance(footer, Mapping):
        raise ValidationError("Embed footer must be a mapping.")

    for field_name, value in footer.items():
        if field_name not in field_validators:
            raise ValidationError(f"Unknown embed footer field: {field_name!r}.")

        for validator in field_validators[field_name]:
            validator(value)


def validate_tag_embed_author(author):
    field_validators = {
        'name': (
            MinLengthValidator(
                limit_value=1,
                message="Embed author name must not be empty."
            ),
            MaxLengthValidator(limit_value=256)
        ),
        'url': (),
        'icon_url': (),
        'proxy_icon_url': ()
    }

    if not isinstance(author, Mapping):
        raise ValidationError("Embed author must be a mapping.")

    for field_name, value in author.items():
        if field_name not in field_validators:
            raise ValidationError(f"Unknown embed author field: {field_name!r}.")

        for validator in field_validators[field_name]:
            validator(value)


def validate_tag_embed(embed):
    """
    Validate a JSON document containing an embed as possible to send
    on Discord. This attempts to rebuild the validation used by Discord
    as well as possible by checking for various embed limits so we can
    ensure that any embed we store here will also be accepted as a
    valid embed by the Discord API.

    Using this directly is possible, although not intended - you usually
    stick this onto the `validators` keyword argument of model fields.

    Example:

        >>> from django.contrib.postgres import fields as pgfields
        >>> from django.db import models
        >>> from api.validators import validate_tag_embed
        >>> class MyMessage(models.Model):
        ...     embed = pgfields.JSONField(
        ...         validators=(
        ...             validate_tag_embed,
        ...         )
        ...     )
        ...     # ...
        ...

    Args:
        embed (Dict[str, Union[str, List[dict], dict]]):
            A dictionary describing the contents of this embed.
            See the official documentation for a full reference
            of accepted keys by this dictionary:
                https://discordapp.com/developers/docs/resources/channel#embed-object

    Raises:
        ValidationError:
            In case the given embed is deemed invalid, a `ValidationError`
            is raised which in turn will allow Django to display errors
            as appropriate.
    """

    all_keys = {
        'title', 'type', 'description', 'url', 'timestamp',
        'color', 'footer', 'image', 'thumbnail', 'video',
        'provider', 'author', 'fields'
    }
    one_required_of = {'content', 'fields', 'image', 'title', 'video'}
    field_validators = {
        'title': (
            MinLengthValidator(
                limit_value=1,
                message="Embed title must not be empty."
            ),
            MaxLengthValidator(limit_value=256)
        ),
        'description': (MaxLengthValidator(limit_value=2048),),
        'fields': (
            MaxLengthValidator(limit_value=25),
            validate_tag_embed_fields
        ),
        'footer': (validate_tag_embed_footer,),
        'author': (validate_tag_embed_author,)
    }

    if not embed:
        raise ValidationError("Tag embed must not be empty.")

    elif not isinstance(embed, Mapping):
        raise ValidationError("Tag embed must be a mapping.")

    elif not any(field in embed for field in one_required_of):
        raise ValidationError(f"Tag embed must contain one of the fields {one_required_of}.")

    for required_key in one_required_of:
        if required_key in embed and not embed[required_key]:
            raise ValidationError(f"Key {required_key!r} must not be empty.")

    for field_name, value in embed.items():
        if field_name not in all_keys:
            raise ValidationError(f"Unknown field name: {field_name!r}")

        if field_name in field_validators:
            for validator in field_validators[field_name]:
                validator(value)
