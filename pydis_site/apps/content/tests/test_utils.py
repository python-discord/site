import datetime
import json
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

_time = datetime.datetime(2022, 10, 10, 10, 10, 10, tzinfo=datetime.timezone.utc)
_time_str = _time.strftime(settings.GITHUB_TIMESTAMP_FORMAT)
TEST_COMMIT_KWARGS = {
    "sha": "123",
    "message": "Hello world\n\nThis is a commit message",
    "date": _time,
    "authors": json.dumps([
        {"name": "Author 1", "email": "mail1@example.com", "date": _time_str},
        {"name": "Author 2", "email": "mail2@example.com", "date": _time_str},
    ]),
}


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

    def setUp(self) -> None:
        super().setUp()
        self.commit = models.Commit.objects.create(**TEST_COMMIT_KWARGS)

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

    @mock.patch("httpx.Client.get")
    def test_mocked_fetch(self, get_mock: mock.Mock):
        """Test that proper data is returned from fetch, but with a mocked API response."""
        fake_request = httpx.Request("GET", "https://google.com")

        # Metadata requests
        returns = [httpx.Response(
            request=fake_request,
            status_code=200,
            json=[
                {"type": "file", "name": "first_tag.md", "sha": "123"},
                {"type": "file", "name": "second_tag.md", "sha": "456"},
                {"type": "dir", "name": "some_group", "sha": "789", "url": "/some_group"},
            ]
        ), httpx.Response(
            request=fake_request,
            status_code=200,
            json=[{"type": "file", "name": "grouped_tag.md", "sha": "789123"}]
        )]

        # Main content request
        bodies = (
            "This is the first tag!",
            textwrap.dedent("""
                ---
                frontmatter: empty
                ---
                This tag has frontmatter!
            """),
            "This is a grouped tag!",
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

                group_folder = tags_folder / "some_group"
                group_folder.mkdir()
                (group_folder / "grouped_tag.md").write_text(bodies[2])

                with tarfile.open(tar_folder / "temp.tar", "w") as file:
                    file.add(folder, recursive=True)

                body = (tar_folder / "temp.tar").read_bytes()

        returns.append(httpx.Response(
            status_code=200,
            content=body,
            request=fake_request,
        ))

        get_mock.side_effect = returns
        result = utils.fetch_tags()

        def sort(_tag: models.Tag) -> str:
            return _tag.name

        self.assertEqual(sorted([
            models.Tag(name="first_tag", body=bodies[0], sha="123"),
            models.Tag(name="second_tag", body=bodies[1], sha="245"),
            models.Tag(name="grouped_tag", body=bodies[2], group=group_folder.name, sha="789123"),
        ], key=sort), sorted(result, key=sort))

    def test_get_real_tag(self):
        """Test that a single tag is returned if it exists."""
        tag = models.Tag.objects.create(name="real-tag", last_commit=self.commit)
        result = utils.get_tag("real-tag")

        self.assertEqual(tag, result)

    def test_get_grouped_tag(self):
        """Test fetching a tag from a group."""
        tag = models.Tag.objects.create(
            name="real-tag", group="real-group", last_commit=self.commit
        )
        result = utils.get_tag("real-group/real-tag")

        self.assertEqual(tag, result)

    def test_get_group(self):
        """Test fetching a group of tags."""
        included = [
            models.Tag.objects.create(name="tag-1", group="real-group"),
            models.Tag.objects.create(name="tag-2", group="real-group"),
            models.Tag.objects.create(name="tag-3", group="real-group"),
        ]

        models.Tag.objects.create(name="not-included-1")
        models.Tag.objects.create(name="not-included-2", group="other-group")

        result = utils.get_tag("real-group")
        self.assertListEqual(included, result)

    def test_get_tag_404(self):
        """Test that an error is raised when we fetch a non-existing tag."""
        models.Tag.objects.create(name="real-tag")
        with self.assertRaises(models.Tag.DoesNotExist):
            utils.get_tag("fake")

    @mock.patch.object(utils, "get_tag_category")
    def test_category_pages(self, get_mock: mock.Mock):
        """Test that the category pages function calls the correct method for tags."""
        tag = models.Tag.objects.create(name="tag")
        get_mock.return_value = tag
        result = utils.get_category_pages(settings.CONTENT_PAGES_PATH / "tags")
        self.assertEqual(tag, result)
        get_mock.assert_called_once_with(collapse_groups=True)

    def test_get_category_root(self):
        """Test that all tags are returned and formatted properly for the tag root page."""
        body = "normal body"
        base = {"description": markdown.markdown(body), "icon": "fas fa-tag"}

        models.Tag.objects.create(name="tag-1", body=body),
        models.Tag.objects.create(name="tag-2", body=body),
        models.Tag.objects.create(name="tag-3", body=body),

        models.Tag.objects.create(name="tag-4", body=body, group="tag-group")
        models.Tag.objects.create(name="tag-5", body=body, group="tag-group")

        result = utils.get_tag_category(collapse_groups=True)

        self.assertDictEqual({
            "tag-1": {**base, "title": "tag-1"},
            "tag-2": {**base, "title": "tag-2"},
            "tag-3": {**base, "title": "tag-3"},
            "tag-group": {
                "title": "tag-group",
                "description": "Contains the following tags: tag-4, tag-5",
                "icon": "fas fa-tags"
            }
        }, result)

    def test_get_category_group(self):
        """Test the function for a group root page."""
        body = "normal body"
        base = {"description": markdown.markdown(body), "icon": "fas fa-tag"}

        included = [
            models.Tag.objects.create(name="tag-1", body=body, group="group"),
            models.Tag.objects.create(name="tag-2", body=body, group="group"),
        ]
        models.Tag.objects.create(name="not-included", body=body)

        result = utils.get_tag_category(included, collapse_groups=False)
        self.assertDictEqual({
            "tag-1": {**base, "title": "tag-1"},
            "tag-2": {**base, "title": "tag-2"},
        }, result)

    def test_tag_url(self):
        """Test that tag URLs are generated correctly."""
        cases = [
            ({"name": "tag"}, f"{models.Tag.URL_BASE}/tag.md"),
            ({"name": "grouped", "group": "abc"}, f"{models.Tag.URL_BASE}/abc/grouped.md"),
        ]

        for options, url in cases:
            tag = models.Tag(**options)
            with self.subTest(tag=tag):
                self.assertEqual(url, tag.url)

    @mock.patch("httpx.Client.get")
    def test_get_tag_commit(self, get_mock: mock.Mock):
        """Test the get commit function with a normal tag."""
        tag = models.Tag.objects.create(name="example")

        authors = json.loads(self.commit.authors)

        get_mock.return_value = httpx.Response(
            request=httpx.Request("GET", "https://google.com"),
            status_code=200,
            json=[{
                "sha": self.commit.sha,
                "commit": {
                    "message": self.commit.message,
                    "author": authors[0],
                    "committer": authors[1],
                }
            }]
        )

        result = utils.get_tag(tag.name)
        self.assertEqual(tag, result)

        get_mock.assert_called_once()
        call_params = get_mock.call_args[1]["params"]

        self.assertEqual({"path": "/bot/resources/tags/example.md"}, call_params)
        self.assertEqual(self.commit, models.Tag.objects.get(name=tag.name).last_commit)

    @mock.patch("httpx.Client.get")
    def test_get_group_tag_commit(self, get_mock: mock.Mock):
        """Test the get commit function with a group tag."""
        tag = models.Tag.objects.create(name="example", group="group-name")

        authors = json.loads(self.commit.authors)
        authors.pop()
        self.commit.authors = json.dumps(authors)
        self.commit.save()

        get_mock.return_value = httpx.Response(
            request=httpx.Request("GET", "https://google.com"),
            status_code=200,
            json=[{
                "sha": self.commit.sha,
                "commit": {
                    "message": self.commit.message,
                    "author": authors[0],
                    "committer": authors[0],
                }
            }]
        )

        utils.set_tag_commit(tag)

        get_mock.assert_called_once()
        call_params = get_mock.call_args[1]["params"]

        self.assertEqual({"path": "/bot/resources/tags/group-name/example.md"}, call_params)
        self.assertEqual(self.commit, models.Tag.objects.get(name=tag.name).last_commit)

    @mock.patch.object(utils, "set_tag_commit")
    def test_exiting_commit(self, set_commit_mock: mock.Mock):
        """Test that a commit is saved when the data has not changed."""
        tag = models.Tag.objects.create(name="tag-name", body="old body", last_commit=self.commit)

        # This is only applied to the object, not to the database
        tag.last_commit = None

        utils.record_tags([tag])
        self.assertEqual(self.commit, tag.last_commit)

        result = utils.get_tag("tag-name")
        self.assertEqual(tag, result)
        set_commit_mock.assert_not_called()
