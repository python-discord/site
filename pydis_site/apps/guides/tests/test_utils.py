import os
from unittest.mock import patch

from django.conf import settings
from django.http import Http404
from django.test import TestCase
from markdown import Markdown

from pydis_site.apps.guides import utils


class TestGetCategory(TestCase):
    def test_get_category_successfully(self):
        """Check does this get right data from category data file."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            result = utils.get_category("category")

        self.assertEqual(result, {"name": "My Category", "description": "My Description"})

    def test_get_category_not_exists(self):
        """Check does this raise 404 error when category don't exists."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            with self.assertRaises(Http404):
                utils.get_category("invalid")

    def test_get_category_not_directory(self):
        """Check does this raise 404 error when category isn't directory."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "test.md")
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            with self.assertRaises(Http404):
                utils.get_category("test.md")


class TestGetCategories(TestCase):
    def test_get_categories(self):
        """Check does this return test guides categories."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")

        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            result = utils.get_categories()

        self.assertEqual(result, {"category": {"name": "My Category", "description": "My Description"}})


class TestGetGuides(TestCase):
    def test_get_all_root_guides(self):
        """Check does this return all root level testing guides."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")

        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            result = utils.get_guides()

        for case in ["test", "test2"]:
            with self.subTest(guide=case):
                md = Markdown(extensions=['meta'])
                with open(os.path.join(path, f"{case}.md")) as f:
                    md.convert(f.read())

                self.assertIn(case, result)
                self.assertEqual(md.Meta, result[case])

    def test_get_all_category_guides(self):
        """Check does this return all category testing guides."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")

        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=path):
            result = utils.get_guides("category")

        md = Markdown(extensions=['meta'])
        with open(os.path.join(path, "category", "test3.md")) as f:
            md.convert(f.read())

        self.assertIn("test3", result)
        self.assertEqual(md.Meta, result["test3"])
