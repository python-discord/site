from unittest.mock import Mock

from django.test import TestCase
from django.template import Template, Context
from wiki.models import URLPath as _URLPath


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
