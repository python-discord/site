from unittest.mock import Mock, create_autospec

from django.forms import (
    BooleanField, BoundField, CharField, ChoiceField, Field, Form, ImageField,
    ModelChoiceField
)
from django.template import Context, Template
from django.test import TestCase
from wiki.editors.markitup import MarkItUpWidget
from wiki.forms import WikiSlugField
from wiki.models import Article, URLPath as _URLPath
from wiki.plugins.notifications.forms import SettingsModelChoiceField

from pydis_site.apps.home.templatetags import wiki_extra

URLPath = Mock(_URLPath)


class TestURLPathFilter(TestCase):
    TEMPLATE = Template(
        """
        {% load wiki_extra %}
        {{ obj|render_urlpath }}
        """
    )

    def test_str(self):
        context = {"obj": "/path/"}
        rendered = self.TEMPLATE.render(Context(context))

        self.assertEqual(rendered.strip(), "/path/")

    def test_str_empty(self):
        context = {"obj": ""}
        rendered = self.TEMPLATE.render(Context(context))

        self.assertEqual(rendered.strip(), "/")

    def test_urlpath(self):
        url_path = URLPath()
        url_path.path = "/path/"

        context = {"obj": url_path}
        rendered = self.TEMPLATE.render(Context(context))

        self.assertEqual(rendered.strip(), "/path/")

    def test_urlpath_root(self):
        url_path = URLPath()
        url_path.path = None

        context = {"obj": url_path}
        rendered = self.TEMPLATE.render(Context(context))

        self.assertEqual(rendered.strip(), "/")


class TestRenderField(TestCase):
    TEMPLATE = Template(
        """
        {% load wiki_extra %}
        {% render_field field %}
        """
    )

    TEMPLATE_NO_LABELS = Template(
        """
        {% load wiki_extra %}
        {% render_field field render_labels=False %}
        """
    )

    TEMPLATE_LABELS_NOT_BOOLEAN = Template(
        """
        {% load wiki_extra %}
        {% render_field field render_labels="" %}
        """
    )

    def test_bound_field(self):
        unbound_field = Field()
        field = BoundField(Form(), unbound_field, "field")

        context = Context({"field": field})
        self.TEMPLATE.render(context)

    def test_bound_field_no_labels(self):
        unbound_field = Field()
        field = BoundField(Form(), unbound_field, "field")

        context = Context({"field": field})
        self.TEMPLATE_NO_LABELS.render(context)

    def test_bound_field_labels_not_boolean(self):
        unbound_field = Field()
        field = BoundField(Form(), unbound_field, "field")

        context = Context({"field": field})
        self.TEMPLATE_LABELS_NOT_BOOLEAN.render(context)

    def test_unbound_field(self):
        field = Field()

        context = Context({"field": field})
        self.TEMPLATE.render(context)

    def test_unbound_field_no_labels(self):
        field = Field()

        context = Context({"field": field})
        self.TEMPLATE_NO_LABELS.render(context)

    def test_unbound_field_labels_not_boolean(self):
        field = Field()

        context = Context({"field": field})
        self.TEMPLATE_LABELS_NOT_BOOLEAN.render(context)


class TestRenderFieldTypes(TestCase):
    TEMPLATE = Template(
        """
        {% load wiki_extra %}
        {% render_field field %}
        """
    )

    @classmethod
    def setUpClass(cls):
        cls._wiki_extra_render = wiki_extra.render
        wiki_extra.render = create_autospec(wiki_extra.render, return_value="")

    @classmethod
    def tearDownClass(cls):
        wiki_extra.render = cls._wiki_extra_render
        del cls._wiki_extra_render

    def test_field_boolean(self):
        field = BooleanField()

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/boolean.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_char(self):
        field = CharField()
        field.widget = None

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/char.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_char_markitup(self):
        field = CharField()
        field.widget = MarkItUpWidget()

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/char.html"
        context = {"field": field, "is_markitup": True, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_image(self):
        field = ImageField()

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/image.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_model_choice(self):
        field = ModelChoiceField(Article.objects.all())

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/model_choice.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_settings_model_choice(self):
        field = SettingsModelChoiceField(Article.objects.all())

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/model_choice.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)

    def test_field_wiki_slug(self):
        field = WikiSlugField()

        context = Context({"field": field})
        self.TEMPLATE.render(context)

        template_path = "wiki/forms/fields/wiki_slug_render.html"
        context = {"field": field, "is_markitup": False, "render_labels": True}

        wiki_extra.render.assert_called_with(template_path, context)


class TestGetFieldOptions(TestCase):
    TEMPLATE = Template(
        """
        {% load wiki_extra %}
        {% get_field_options field %}
        """
    )

    def test_get_field_options(self):
        unbound_field = ChoiceField()
        field = BoundField(Form(), unbound_field, "field")

        context = Context({"field": field})
        self.TEMPLATE.render(context)

    def test_get_field_options_value(self):
        unbound_field = ChoiceField()
        field = BoundField(Form(initial={"field": "Value"}), unbound_field, "field")

        context = Context({"field": field})
        self.TEMPLATE.render(context)
