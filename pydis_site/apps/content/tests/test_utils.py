from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

from dateutil.parser import isoparse
from django.conf import settings
from django.http import Http404
from django.test import TestCase
from markdown2 import markdown

from pydis_site.apps.content import utils

BASE_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "content", "tests", "test_content")


class TestGetBasePath(TestCase):
    def test_get_base_path(self):
        """Test does function return content base path."""
        self.assertEqual(
            utils._get_base_path(),
            Path(settings.BASE_DIR, "pydis_site", "apps", "content", "resources", "content")
        )


class TestGetCategory(TestCase):
    def test_get_category_successfully(self):
        """Check does this get right data from category data file."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_category("category")

        self.assertEqual(result, {"name": "My Category", "description": "My Description"})

    def test_get_category_not_exists(self):
        """Check does this raise 404 error when category don't exists."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_category("invalid")

    def test_get_category_not_directory(self):
        """Check does this raise 404 error when category isn't directory."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_category("test.md")


class TestGetCategories(TestCase):
    def test_get_categories(self):
        """Check does this return test content categories."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_categories()

        self.assertEqual(
            result, {"category": {"name": "My Category", "description": "My Description"}}
        )


class TestGetArticles(TestCase):
    def test_get_all_root_articles(self):
        """Check does this return all root level testing content."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_articles()

        for case in ["test", "test2"]:
            with self.subTest(guide=case):
                md = markdown(BASE_PATH.joinpath(f"{case}.md").read_text(), extras=["metadata"])

                self.assertIn(case, result)
                self.assertEqual(md.metadata, result[case])

    def test_get_all_category_articles(self):
        """Check does this return all category testing content."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_articles("category")

        md = markdown(BASE_PATH.joinpath("category", "test3.md").read_text(), extras=["metadata"])

        self.assertIn("test3", result)
        self.assertEqual(md.metadata, result["test3"])


class TestGetArticle(TestCase):
    def test_get_root_article_success(self):
        """Check does this return article HTML and metadata when root article exist."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_article("test", None)

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

        self.assertEqual(result, {"article": str(md), "metadata": md.metadata})

    def test_get_root_article_dont_exist(self):
        """Check does this raise Http404 when root article don't exist."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_article("invalid", None)

    def test_get_category_article_success(self):
        """Check does this return article HTML and metadata when category guide exist."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            result = utils.get_article("test3", "category")

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

        self.assertEqual(result, {"article": str(md), "metadata": md.metadata})

    def test_get_category_article_dont_exist(self):
        """Check does this raise Http404 when category article don't exist."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_article("invalid", "category")

    def test_get_category_article_category_dont_exist(self):
        """Check does this raise Http404 when category don't exist."""
        with patch("pydis_site.apps.content.utils._get_base_path", return_value=BASE_PATH):
            with self.assertRaises(Http404):
                utils.get_article("some-guide", "invalid")


class GetGitHubInformationTests(TestCase):
    @patch("pydis_site.apps.content.utils.requests.get")
    @patch("pydis_site.apps.content.utils.COMMITS_URL", "foobar")
    def test_call_get_github_information_requests_get(self, requests_get_mock):
        """Check does this call requests.get function with proper URL."""
        utils.get_github_information("foo", None)
        requests_get_mock.assert_called_once_with("foobar")

    @patch("pydis_site.apps.content.utils.requests.get")
    def test_github_status_code_200_response(self, requests_get_mock):
        """Check does this return provided modified date and contributors."""
        requests_get_mock.return_value = MagicMock(status_code=200)
        requests_get_mock.return_value.json.return_value = [{
            "commit": {
                "committer": {
                    "date": datetime(2020, 10, 1).isoformat(),
                    "name": "foobar",
                }
            },
            "committer": {
                "html_url": "abc1234"
            }
        }]
        result = utils.get_github_information("foo", None)
        self.assertEqual(result, {
            "last_modified": datetime(2020, 10, 1).strftime("%dth %B %Y"),
            "contributors": {"foobar": "abc1234"}
        })

    @patch("pydis_site.apps.content.utils.requests.get")
    def test_github_other_status_code_response(self, requests_get_mock):
        """Check does this return provided modified date and contributors."""
        requests_get_mock.return_value = MagicMock(status_code=404)
        result = utils.get_github_information("foo", None)
        self.assertEqual(result, {
            "last_modified": "N/A",
            "contributors": {}
        })
