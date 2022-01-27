from django import template

register = template.Library()


@register.filter
def as_css_class(class_name: str) -> str:
    """
    Convert any string to a css-class name.

    For example, convert
    "Favorite FROOT_is_LEMON" to
    "favorite-froot-is-lemon"
    """
    class_name = class_name.lower()
    class_name = class_name.replace(" ", "-")
    class_name = class_name.replace("_", "-")
    return class_name
