from datetime import datetime

from django import template

register = template.Library()


@register.filter
def hex_colour(colour: str | int) -> str:
    """
    Converts the given representation of a colour to its RGB hex string.

    As we are using a Discord dark theme analogue, black colours are returned as white instead.
    """
    if isinstance(colour, str):
        colour = colour if colour.startswith("#") else f"#{colour}"
    else:
        colour = f"#{colour:0>6X}"
    return colour if colour != "#000000" else "#FFFFFF"


@register.filter
def footer_datetime(timestamp: str) -> datetime:
    """Takes an embed timestamp and returns a timezone-aware datetime object."""
    return datetime.fromisoformat(timestamp)


@register.filter
def visible_newlines(text: str) -> str:
    """Visualizes newlines in text by replacing them with a grey-ish `↵`."""
    return text.replace("\n", " <span class='has-text-grey'>↵</span><br>")
