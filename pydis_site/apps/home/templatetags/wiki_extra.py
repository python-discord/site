from typing import Any, Dict, Type, Union

from django import template
from django.forms import BooleanField, BoundField, CharField, Field, ImageField, ModelChoiceField
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from wiki.editors.markitup import MarkItUpWidget
from wiki.forms import WikiSlugField
from wiki.models import URLPath
from wiki.plugins.notifications.forms import SettingsModelChoiceField

TEMPLATE_PATH = "wiki/forms/fields/{0}.html"

TEMPLATES: Dict[Type, str] = {
    BooleanField: TEMPLATE_PATH.format("boolean"),
    CharField: TEMPLATE_PATH.format("char"),
    ImageField: TEMPLATE_PATH.format("image"),

    ModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    SettingsModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    WikiSlugField: TEMPLATE_PATH.format("wiki_slug_render"),
}


register = template.Library()


def get_unbound_field(field: BoundField) -> Field:
    while isinstance(field, BoundField):
        field = field.field

    return field


def render(template_path: str, context: Dict[str, Any]):
    return mark_safe(get_template(template_path).render(context))  # noqa: S703 S308


@register.simple_tag
def render_field(field: Field, render_labels: bool = True):
    if isinstance(field, BoundField):
        unbound_field = get_unbound_field(field)
    else:
        unbound_field = field

    if not isinstance(render_labels, bool):
        render_labels = True

    template_path = TEMPLATES.get(unbound_field.__class__, TEMPLATE_PATH.format("in_place_render"))
    is_markitup = isinstance(unbound_field.widget, MarkItUpWidget)
    context = {"field": field, "is_markitup": is_markitup, "render_labels": render_labels}

    return render(template_path, context)


@register.simple_tag(takes_context=True)
def get_field_options(context: Context, field: BoundField):
    widget = field.field.widget

    if field.value() is None:
        value = []
    else:
        value = [str(field.value())]

    context["options"] = widget.optgroups(field.name, value)
    return ""


@register.filter
def render_urlpath(value: Union[URLPath, str]):
    if isinstance(value, str):
        return value or "/"

    return value.path or "/"
