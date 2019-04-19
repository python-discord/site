from typing import Union

from django import template
from django.forms import (
    BooleanField, BoundField, CharField, ChoiceField, ComboField, DateField, DateTimeField, DecimalField, DurationField,
    EmailField, Field, FileField, FilePathField, FloatField, GenericIPAddressField, ImageField, IntegerField,
    ModelChoiceField, ModelMultipleChoiceField, MultiValueField, MultipleChoiceField, NullBooleanField, RegexField,
    SlugField, SplitDateTimeField, TimeField, TypedChoiceField, TypedMultipleChoiceField, URLField, UUIDField)
from django.template import Template, Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from wiki.editors.markitup import MarkItUpWidget
from wiki.forms import WikiSlugField
from wiki.models import URLPath
from wiki.plugins.notifications.forms import SettingsModelChoiceField

TEMPLATE_PATH = "wiki/forms/fields/{0}.html"

TEMPLATES = {
    BooleanField: TEMPLATE_PATH.format("boolean"),
    CharField: TEMPLATE_PATH.format("char"),
    ChoiceField: TEMPLATE_PATH.format("in_place_render"),
    TypedChoiceField: TEMPLATE_PATH.format("in_place_render"),
    DateField: TEMPLATE_PATH.format("in_place_render"),
    DateTimeField: TEMPLATE_PATH.format("in_place_render"),
    DecimalField: TEMPLATE_PATH.format("in_place_render"),
    DurationField: TEMPLATE_PATH.format("in_place_render"),
    EmailField: TEMPLATE_PATH.format("in_place_render"),
    FileField: TEMPLATE_PATH.format("in_place_render"),
    FilePathField: TEMPLATE_PATH.format("in_place_render"),
    FloatField: TEMPLATE_PATH.format("in_place_render"),
    ImageField: TEMPLATE_PATH.format("image"),
    IntegerField: TEMPLATE_PATH.format("in_place_render"),
    GenericIPAddressField: TEMPLATE_PATH.format("in_place_render"),
    MultipleChoiceField: TEMPLATE_PATH.format("in_place_render"),
    TypedMultipleChoiceField: TEMPLATE_PATH.format("in_place_render"),
    NullBooleanField: TEMPLATE_PATH.format("in_place_render"),
    RegexField: TEMPLATE_PATH.format("in_place_render"),
    SlugField: TEMPLATE_PATH.format("in_place_render"),
    TimeField: TEMPLATE_PATH.format("in_place_render"),
    URLField: TEMPLATE_PATH.format("in_place_render"),
    UUIDField: TEMPLATE_PATH.format("in_place_render"),

    ComboField: TEMPLATE_PATH.format("in_place_render"),
    MultiValueField: TEMPLATE_PATH.format("in_place_render"),
    SplitDateTimeField: TEMPLATE_PATH.format("in_place_render"),

    ModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    ModelMultipleChoiceField: TEMPLATE_PATH.format("in_place_render"),

    SettingsModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    WikiSlugField: TEMPLATE_PATH.format("wiki_slug_render"),
}


register = template.Library()


def get_unbound_field(field: BoundField):
    while isinstance(field, BoundField):
        field = field.field

    return field


@register.simple_tag
def render_field(field: Field, render_labels: bool = True):
    if isinstance(field, BoundField):
        unbound_field = get_unbound_field(field)
    else:
        unbound_field = field

    if not isinstance(render_labels, bool):
        render_labels = True

    template_path = TEMPLATES.get(unbound_field.__class__)
    is_markitup = isinstance(unbound_field.widget, MarkItUpWidget)

    if not template_path:
        raise NotImplementedError(f"Unknown field type: {unbound_field.__class__}")

    template_obj: Template = get_template(template_path)
    context = {"field": field, "is_markitup": is_markitup, "render_labels": render_labels}

    return mark_safe(template_obj.render(context))


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
