import tarfile
import tempfile
import textwrap
from pathlib import Path
from unittest import mock

import httpx
import markdown
from django.http import Http404
from django.test import TestCase

from pydis_site import settings
from pydis_site.apps.content import models, utils
from pydis_site.apps.content.tests.helpers import (
    BASE_PATH, MockPagesTestCase, PARSED_CATEGORY_INFO, PARSED_HTML, PARSED_METADATA
)


class GetCategoryTests(MockPagesTestCase):
    """Tests for the get_category function."""

    def test_get_valid_category(self):
        result = utils.get_category(Path(BASE_PATH, "category"))

        self.assertEqual(result, {"title": "Category Name", "description": "Description"})

    def test_get_nonexistent_category(self):
        with self.assertRaises(Http404):
            utils.get_category(Path(BASE_PATH, "invalid"))

    def test_get_category_with_path_to_file(self):
        # Valid categories are directories, not files
        with self.assertRaises(Http404):
            utils.get_category(Path(BASE_PATH, "root.md"))

    def test_get_category_without_info_yml(self):
        # Categories should provide an _info.yml file
        with self.assertRaises(FileNotFoundError):
            utils.get_category(Path(BASE_PATH, "tmp/category/subcategory_without_info"))


class GetCategoriesTests(MockPagesTestCase):
    """Tests for the get_categories function."""

    def test_get_root_categories(self):
        result = utils.get_categories(BASE_PATH)

        info = PARSED_CATEGORY_INFO
        categories = {
            "category": info,
            "tmp": info,
            "not_a_page.md": info,
        }
        self.assertEqual(result, categories)

    def test_get_categories_with_subcategories(self):
        result = utils.get_categories(Path(BASE_PATH, "category"))

        self.assertEqual(result, {"subcategory": PARSED_CATEGORY_INFO})

    def test_get_categories_without_subcategories(self):
        result = utils.get_categories(Path(BASE_PATH, "category/subcategory"))

        self.assertEqual(result, {})


class GetCategoryPagesTests(MockPagesTestCase):
    """Tests for the get_category_pages function."""

    def test_get_pages_in_root_category_successfully(self):
        """The method should successfully retrieve page metadata."""
        root_category_pages = utils.get_category_pages(BASE_PATH)
        self.assertEqual(
            root_category_pages, {"root": PARSED_METADATA, "root_without_metadata": {}}
        )

    def test_get_pages_in_subcategories_successfully(self):
        """The method should successfully retrieve page metadata."""
        category_pages = utils.get_category_pages(Path(BASE_PATH, "category"))

        # Page metadata is properly retrieved
        self.assertEqual(category_pages, {"with_metadata": PARSED_METADATA})


class GetPageTests(MockPagesTestCase):
    """Tests for the get_page function."""

    def test_get_page(self):
        # TOC is a special case because the markdown converter outputs the TOC as HTML
        updated_metadata = {**PARSED_METADATA, "toc": '<div class="toc">\n<ul></ul>\n</div>\n'}
        cases = [
            ("Root page with metadata", "root.md", PARSED_HTML, updated_metadata),
            ("Root page without metadata", "root_without_metadata.md", PARSED_HTML, {}),
            ("Page with metadata", "category/with_metadata.md", PARSED_HTML, updated_metadata),
            ("Page without metadata", "category/subcategory/without_metadata.md", PARSED_HTML, {}),
        ]

        for msg, page_path, expected_html, expected_metadata in cases:
            with self.subTest(msg=msg):
                html, metadata = utils.get_page(Path(BASE_PATH, page_path))
                self.assertEqual(html, expected_html)
                self.assertEqual(metadata, expected_metadata)

    def test_get_nonexistent_page_returns_404(self):
        with self.assertRaises(Http404):
            utils.get_page(Path(BASE_PATH, "invalid"))


class TagUtilsTests(TestCase):
    """Tests for the tag-related utilities."""

    @mock.patch.object(utils, "fetch_tags")
    def test_static_fetch(self, fetch_mock: mock.Mock):
        """Test that the static fetch function is only called at most once during static builds."""
        tags = [models.Tag(name="Name", body="body")]
        fetch_mock.return_value = tags
        result = utils.get_tags_static()
        second_result = utils.get_tags_static()

        fetch_mock.assert_called_once()
        self.assertEqual(tags, result)
        self.assertEqual(tags, second_result)

    @mock.patch("httpx.get")
    def test_mocked_fetch(self, get_mock: mock.Mock):
        """Test that proper data is returned from fetch, but with a mocked API response."""
        bodies = (
            "This is the first tag!",
            textwrap.dedent("""
                ---
                frontmatter: empty
                ---
                This tag has frontmatter!
            """),
        )

        # Generate a tar archive with a few tags
        with tempfile.TemporaryDirectory() as tar_folder:
            tar_folder = Path(tar_folder)
            with tempfile.TemporaryDirectory() as folder:
                folder = Path(folder)
                (folder / "ignored_file.md").write_text("This is an ignored file.")
                tags_folder = folder / "bot/resources/tags"
                tags_folder.mkdir(parents=True)

                (tags_folder / "first_tag.md").write_text(bodies[0])
                (tags_folder / "second_tag.md").write_text(bodies[1])

                with tarfile.open(tar_folder / "temp.tar", "w") as file:
                    file.add(folder, recursive=True)

                body = (tar_folder / "temp.tar").read_bytes()

        get_mock.return_value = httpx.Response(
            status_code=200,
            content=body,
            request=httpx.Request("GET", "https://google.com"),
        )

        result = utils.fetch_tags()
        self.assertEqual([
            models.Tag(name="first_tag", body=bodies[0]),
            models.Tag(name="second_tag", body=bodies[1]),
        ], sorted(result, key=lambda tag: tag.name))

    def test_get_real_tag(self):
        """Test that a single tag is returned if it exists."""
        tag = models.Tag.objects.create(name="real-tag")
        result = utils.get_tag("real-tag")

        self.assertEqual(tag, result)

    def test_get_tag_404(self):
        """Test that an error is raised when we fetch a non-existing tag."""
        models.Tag.objects.create(name="real-tag")
        with self.assertRaises(models.Tag.DoesNotExist):
            utils.get_tag("fake")

    def test_category_pages(self):
        """Test that the category pages function returns the correct records for tags."""
        models.Tag.objects.create(name="second-tag", body="Normal body")
        models.Tag.objects.create(name="first-tag", body="Normal body")
        tag_body = {"description": markdown.markdown("Normal body"), "icon": "fas fa-tag"}

        result = utils.get_category_pages(settings.CONTENT_PAGES_PATH / "tags")
        self.assertDictEqual({
            "first-tag": {**tag_body, "title": "first-tag"},
            "second-tag": {**tag_body, "title": "second-tag"},
        }, result)

    def test_trimmed_tag_content(self):
        """Test a tag with a long body that requires trimming."""
        tag = models.Tag.objects.create(name="long-tag", body="E" * 300)
        result = utils.get_category_pages(settings.CONTENT_PAGES_PATH / "tags")
        self.assertDictEqual({"long-tag": {
            "title": "long-tag",
            "description": markdown.markdown(tag.body[:100] + "..."),
            "icon": "fas fa-tag",
        }}, result)
