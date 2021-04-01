from django.test import TestCase

from pydis_site.apps.content.templatetags.str_methods import replace_hyphens


class TestTemplateTags(TestCase):
    """Tests for the custom template tags in the content app."""

    def test_replace_hyphens(self):
        self.assertEquals(replace_hyphens("word-with-hyphens", " "), "word with hyphens")
        self.assertEquals(replace_hyphens("---", ""), "")
        self.assertEquals(replace_hyphens("hi----", "A"), "hiAAAA")
