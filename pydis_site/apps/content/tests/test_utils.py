from pathlib import Path

from django.http import Http404

from pydis_site.apps.content import utils
from pydis_site.apps.content.tests.helpers import (
    MockPagesTestCase, PARSED_CATEGORY_INFO, PARSED_HTML, PARSED_METADATA
)


class GetCategoryTests(MockPagesTestCase):
    """Tests for the get_category function."""

    def test_get_valid_category(self):
        result = utils.get_category(Path("category"))

        self.assertEqual(result, {"name": "Category Name", "description": "Description"})

    def test_get_nonexistent_category(self):
        with self.assertRaises(Http404):
            utils.get_category(Path("invalid"))

    def test_get_category_with_path_to_file(self):
        # Valid categories are directories, not files
        with self.assertRaises(Http404):
            utils.get_category(Path("root.md"))

    def test_get_category_without_info_yml(self):
        # Categories should provide an _info.yml file
        with self.assertRaises(FileNotFoundError):
            utils.get_category(Path("tmp/category_without_info"))


class GetCategoriesTests(MockPagesTestCase):
    """Tests for the get_categories function."""

    def test_get_root_categories(self):
        result = utils.get_categories(Path("."))

        info = PARSED_CATEGORY_INFO
        self.assertEqual(result, {"category": info, "tmp": info, "not_a_page.md": info})

    def test_get_categories_with_subcategories(self):
        result = utils.get_categories(Path("category"))

        self.assertEqual(result, {"subcategory": PARSED_CATEGORY_INFO})

    def test_get_categories_without_subcategories(self):
        result = utils.get_categories(Path("category/subcategory"))

        self.assertEqual(result, {})


class GetCategoryPagesTests(MockPagesTestCase):
    """Tests for the get_category_pages function."""

    def test_get_pages_in_root_category_successfully(self):
        """The method should successfully retrieve page metadata."""
        root_category_pages = utils.get_category_pages(Path("."))
        self.assertEqual(
            root_category_pages, {"root": PARSED_METADATA, "root_without_metadata": {}}
        )

    def test_get_pages_in_subcategories_successfully(self):
        """The method should successfully retrieve page metadata."""
        category_pages = utils.get_category_pages(Path("category"))

        # Page metadata is properly retrieved
        self.assertEqual(category_pages, {"with_metadata": PARSED_METADATA})


class GetPageTests(MockPagesTestCase):
    """Tests for the get_page function."""

    def test_get_page(self):
        cases = [
            ("Root page with metadata", "root.md", PARSED_HTML, PARSED_METADATA),
            ("Root page without metadata", "root_without_metadata.md", PARSED_HTML, {}),
            ("Page with metadata", "category/with_metadata.md", PARSED_HTML, PARSED_METADATA),
            ("Page without metadata", "category/subcategory/without_metadata.md", PARSED_HTML, {}),
        ]

        for msg, page_path, expected_html, expected_metadata in cases:
            with self.subTest(msg=msg):
                html, metadata = utils.get_page(Path(page_path))
                self.assertEqual(html, expected_html)
                self.assertEqual(metadata, expected_metadata)

    def test_get_nonexistent_page_returns_404(self):
        with self.assertRaises(Http404):
            utils.get_page(Path("invalid"))
