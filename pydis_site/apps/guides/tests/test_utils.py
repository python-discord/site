import os
from unittest.mock import patch

from django.conf import settings
from django.http import Http404
from django.test import TestCase
from markdown import Markdown

from pydis_site.apps.guides import utils

BASE_PATH = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")


class TestGetBasePath(TestCase):
    def test_get_base_path(self):
        """Test does function return guides base path."""
        self.assertEqual(
            utils._get_base_path(),
            os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "resources", "guides")
        )


class TestGetCategory(TestCase):
    def test_get_category_successfully(self):
        """Check does this get right data from category data file."""
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_category("category")

        self.assertEqual(result, {"name": "My Category", "description": "My Description"})

    def test_get_category_not_exists(self):
        """Check does this raise 404 error when category don't exists."""
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_category("invalid")

    def test_get_category_not_directory(self):
        """Check does this raise 404 error when category isn't directory."""
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_category("test.md")


class TestGetCategories(TestCase):
    def test_get_categories(self):
        """Check does this return test guides categories."""
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_categories()

        self.assertEqual(result, {"category": {"name": "My Category", "description": "My Description"}})


class TestGetGuides(TestCase):
    def test_get_all_root_guides(self):
        """Check does this return all root level testing guides."""
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
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
        with patch("pydis_site.apps.guides.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_guides("category")

        md = Markdown(extensions=['meta'])
        with open(os.path.join(BASE_PATH, "category", "test3.md")) as f:
            md.convert(f.read())

        self.assertIn("test3", result)
        self.assertEqual(md.Meta, result["test3"])
