from django.test import TestCase

from pydis_site.apps.resources.templatetags.to_kebabcase import _to_kebabcase


class TestToKebabcase(TestCase):
    """Tests for the `as_css_class` template tag."""

    def test_to_kebabcase(self):
        """Test the to_kebabcase utility and template tag."""
        weird_input = (
            "_-_--_A_LEm0n?in&¤'the##trEE£$@€@€@@£is-NOT----QUITE//"
            "as#good!  as one   __IN-YOUR|||HaND"
        )

        self.assertEqual(
            _to_kebabcase(weird_input),
            "a-lem0n-in-the-tree-is-not-quite-as-good-as-one-in-your-hand",
        )
