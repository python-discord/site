from django.test import TestCase

from pydis_site.apps.home.templatetags import starts_with


class TestTemplateTags(TestCase):
    def test_starts_with(self):
        self.assertTrue(starts_with('foo', 'f'))
