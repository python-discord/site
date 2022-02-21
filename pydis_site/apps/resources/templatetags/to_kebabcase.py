import re

from django import template

REGEX_CONSECUTIVE_NON_LETTERS = r"[^A-Za-z0-9]+"
register = template.Library()


def _to_kebabcase(class_name: str) -> str:
    """
    Convert any string to kebab-case.

    For example, convert
    "__Favorite FROOT¤#/$?is----LeMON???" to
    "favorite-froot-is-lemon"
    """
    # First, make it lowercase, and just remove any apostrophes.
    # We remove the apostrophes because "wasnt" is better than "wasn-t"
    class_name = class_name.casefold()
    class_name = class_name.replace("'", '')

    # Now, replace any non-letter that remains with a dash.
    # If there are multiple consecutive non-letters, just replace them with a single dash.
    # my-favorite-class is better than my-favorite------class
    class_name = re.sub(
        REGEX_CONSECUTIVE_NON_LETTERS,
        "-",
        class_name,
    )

    # Now we use strip to get rid of any leading or trailing dashes.
    class_name = class_name.strip("-")
    return class_name


@register.filter
def to_kebabcase(class_name: str) -> str:
    """Convert a string to kebab-case."""
    return _to_kebabcase(class_name)
