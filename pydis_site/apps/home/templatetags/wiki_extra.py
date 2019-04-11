from django import template
from django.forms import (
    BooleanField, CharField, ChoiceField, ComboField, DateField, DateTimeField, DecimalField, DurationField, EmailField,
    Field, FileField, FilePathField, FloatField, GenericIPAddressField, ImageField, IntegerField, ModelChoiceField,
    ModelMultipleChoiceField, MultiValueField, MultipleChoiceField, NullBooleanField, RegexField, SlugField,
    SplitDateTimeField, TimeField, TypedChoiceField, TypedMultipleChoiceField, URLField, UUIDField, BoundField)
from django.template import Template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from wiki.editors.markitup import MarkItUpWidget

TEMPLATE_PATH = "wiki/forms/fields/{0}.html"

TEMPLATES = {
    BooleanField: TEMPLATE_PATH.format("boolean"),
    CharField: TEMPLATE_PATH.format("char"),
    ChoiceField: TEMPLATE_PATH.format("choice"),
    TypedChoiceField: TEMPLATE_PATH.format("typed_choice"),
    DateField: TEMPLATE_PATH.format("date"),
    DateTimeField: TEMPLATE_PATH.format("date_time"),
    DecimalField: TEMPLATE_PATH.format("decimal"),
    DurationField: TEMPLATE_PATH.format("duration"),
    EmailField: TEMPLATE_PATH.format("email"),
    FileField: TEMPLATE_PATH.format("file"),
    FilePathField: TEMPLATE_PATH.format("file_path"),
    FloatField: TEMPLATE_PATH.format("float"),
    ImageField: TEMPLATE_PATH.format("image"),
    IntegerField: TEMPLATE_PATH.format("integer"),
    GenericIPAddressField: TEMPLATE_PATH.format("generic_ip_address"),
    MultipleChoiceField: TEMPLATE_PATH.format("multiple_choice"),
    TypedMultipleChoiceField: TEMPLATE_PATH.format("typed_multiple_choice"),
    NullBooleanField: TEMPLATE_PATH.format("null_boolean"),
    RegexField: TEMPLATE_PATH.format("regex"),
    SlugField: TEMPLATE_PATH.format("slug"),
    TimeField: TEMPLATE_PATH.format("time"),
    URLField: TEMPLATE_PATH.format("url"),
    UUIDField: TEMPLATE_PATH.format("uuid"),

    ComboField: TEMPLATE_PATH.format("combo"),
    MultiValueField: TEMPLATE_PATH.format("multi_value"),
    SplitDateTimeField: TEMPLATE_PATH.format("split_date_time"),

    ModelChoiceField: TEMPLATE_PATH.format("model_choice"),
    ModelMultipleChoiceField: TEMPLATE_PATH.format("model_multiple_choice"),
}


register = template.Library()


@register.simple_tag
def render_field(field: Field):
    if isinstance(field, BoundField):
        template_path = TEMPLATES.get(field.field.__class__)
        is_markitup = isinstance(field.field.widget, MarkItUpWidget)
    else:
        template_path = TEMPLATES.get(field.__class__)
        is_markitup = isinstance(field.widget, MarkItUpWidget)

    if not template_path:
        raise NotImplementedError(f"Unknown field type: {field.__class__}")

    template_obj: Template = get_template(template_path)
    context = {"field": field, "is_markitup": is_markitup}

    return mark_safe(template_obj.render(context))
