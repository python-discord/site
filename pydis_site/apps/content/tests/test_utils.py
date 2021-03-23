from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.http import Http404
from django.test import TestCase, override_settings
from markdown2 import markdown

from pydis_site.apps.content import utils

BASE_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "content", "tests", "test_content")


class TestGetCategory(TestCase):
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_category_successfully(self):
        """Check does this get right data from category data file."""
        result = utils.get_category(["category"])

        self.assertEqual(result, {"name": "My Category", "description": "My Description"})

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_category_not_exists(self):
        """Check does this raise 404 error when category don't exists."""
        with self.assertRaises(Http404):
            utils.get_category(["invalid"])

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_category_not_directory(self):
        """Check does this raise 404 error when category isn't directory."""
        with self.assertRaises(Http404):
            utils.get_category(["test.md"])


class TestGetCategories(TestCase):
    @override_settings(PAGES_PATH=BASE_PATH)
    @patch("pydis_site.apps.content.utils.get_category")
    def test_get_categories(self, get_category_mock):
        """Check does this return test content categories."""
        get_category_mock.return_value = {"name": "My Category", "description": "My Description"}

        result = utils.get_categories()
        get_category_mock.assert_called_once_with(["category"])

        self.assertEqual(
            result, {"category": {"name": "My Category", "description": "My Description"}}
        )

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_categories_root_path(self):
        """Check does this doesn't call joinpath when getting root categories."""
        result = utils.get_categories()
        self.assertEqual(
            result, {"category": {"name": "My Category", "description": "My Description"}}
        )

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_categories_in_category(self):
        """Check does this call joinpath when getting subcategories."""
        result = utils.get_categories(["category"])
        self.assertEqual(
            result, {"subcategory": {"name": "My Category 1", "description": "My Description 1"}}
        )


class TestGetPages(TestCase):
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_all_root_pages(self):
        """Check does this return all root level testing content."""
        result = utils.get_pages()

        for case in ["test", "test2"]:
            with self.subTest(guide=case):
                md = markdown(BASE_PATH.joinpath(f"{case}.md").read_text(), extras=["metadata"])

                self.assertIn(case, result)
                self.assertEqual(md.metadata, result[case])

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_all_category_pages(self):
        """Check does this return all category testing content."""
        result = utils.get_pages(["category"])

        md = markdown(BASE_PATH.joinpath("category", "test3.md").read_text(), extras=["metadata"])

        self.assertIn("test3", result)
        self.assertEqual(md.metadata, result["test3"])


class TestGetPage(TestCase):
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_root_page_success(self):
        """Check does this return page HTML and metadata when root page exist."""
        result = utils.get_page(["test"])

        md = markdown(
            BASE_PATH.joinpath("test.md").read_text(),
            extras=[
                "metadata",
                "fenced-code-blocks",
                "header-ids",
                "strike",
                "target-blank-links",
                "tables",
                "task_list"
            ]
        )

        self.assertEqual(result, {"page": str(md), "metadata": md.metadata})

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_root_page_dont_exist(self):
        """Check does this raise Http404 when root page don't exist."""
        with self.assertRaises(Http404):
            utils.get_page(["invalid"])

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_category_page_success(self):
        """Check does this return page HTML and metadata when category guide exist."""
        result = utils.get_page(["category", "test3"])

        md = markdown(
            BASE_PATH.joinpath("category", "test3.md").read_text(),
            extras=[
                "metadata",
                "fenced-code-blocks",
                "header-ids",
                "strike",
                "target-blank-links",
                "tables",
                "task_list"
            ]
        )

        self.assertEqual(result, {"page": str(md), "metadata": md.metadata})

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_get_category_page_dont_exist(self):
        """Check does this raise Http404 when category page don't exist."""
        with self.assertRaises(Http404):
            utils.get_page(["category", "invalid"])

    @patch("pydis_site.settings.PAGES_PATH", new=BASE_PATH)
    def test_get_category_page_category_dont_exist(self):
        """Check does this raise Http404 when category don't exist."""
        with self.assertRaises(Http404):
            utils.get_page(["invalid", "some-guide"])
