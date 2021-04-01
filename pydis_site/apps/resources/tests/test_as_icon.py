from django.test import TestCase

from pydis_site.apps.resources.templatetags import as_icon


class TestAsIcon(TestCase):
    """Tests for `as_icon` templatetag."""

    def test_as_icon(self):
        """Should return proper icon type class and icon class based on input."""
        test_cases = [
            {
                "input": "regular/icon",
                "output": "fas fa-icon",
            },
            {
                "input": "branding/brand",
                "output": "fab fa-brand",
            },
            {
                "input": "fake/my-icon",
                "output": "fas fa-my-icon",
            }
        ]

        for case in test_cases:
            with self.subTest(input=case["input"], output=case["output"]):
                self.assertEqual(case["output"], as_icon(case["input"]))
