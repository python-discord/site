from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django_hosts.resolvers import reverse

from pydis_site.apps.content.views import ArticleOrCategoryView

BASE_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "content", "tests", "test_content")


class TestArticlesIndexView(TestCase):
    @patch("pydis_site.apps.content.views.articles.get_articles")
    @patch("pydis_site.apps.content.views.articles.get_categories")
    def test_articles_index_return_200(self, get_categories_mock, get_articles_mock):
        """Check that content index return HTTP code 200."""
        get_categories_mock.return_value = {}
        get_articles_mock.return_value = {}

        url = reverse('content:articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_articles_mock.assert_called_once()
        get_categories_mock.assert_called_once()


class TestArticleOrCategoryView(TestCase):
    @override_settings(ARTICLES_PATH=BASE_PATH)
    @patch("pydis_site.apps.content.views.article_category.utils.get_article")
    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @patch("pydis_site.apps.content.views.article_category.utils.get_github_information")
    def test_article_return_code_200(self, gh_info_mock, get_category_mock, get_article_mock):
        get_article_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("content:article_category", args=["test2"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_category_mock.assert_not_called()
        get_article_mock.assert_called_once()
        gh_info_mock.assert_called_once()

    @patch("pydis_site.apps.content.views.article_category.utils.get_article")
    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_article_return_404(self, get_category_mock, get_article_mock):
        """Check that return code is 404 when invalid article provided."""
        get_article_mock.side_effect = Http404("Article not found.")

        url = reverse("content:article_category", args=["invalid-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_article_mock.assert_not_called()
        get_category_mock.assert_not_called()

    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @patch("pydis_site.apps.content.views.article_category.utils.get_articles")
    @patch("pydis_site.apps.content.views.article_category.utils.get_categories")
    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_valid_category_code_200(
            self,
            get_categories_mock,
            get_articles_mock,
            get_category_mock
    ):
        """Check that return code is 200 when visiting valid category."""
        get_category_mock.return_value = {"name": "test", "description": "test"}
        get_articles_mock.return_value = {}

        url = reverse("content:article_category", args=["category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        get_articles_mock.assert_called_once()
        get_category_mock.assert_called_once()
        get_categories_mock.assert_called_once()

    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @patch("pydis_site.apps.content.views.article_category.utils.get_articles")
    @patch("pydis_site.apps.content.views.article_category.utils.get_categories")
    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_invalid_category_code_404(
            self,
            get_categories_mock,
            get_articles_mock,
            get_category_mock
    ):
        """Check that return code is 404 when trying to visit invalid category."""
        get_category_mock.side_effect = Http404("Category not found.")

        url = reverse("content:article_category", args=["invalid-category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        get_category_mock.assert_not_called()
        get_articles_mock.assert_not_called()
        get_categories_mock.assert_not_called()

    @patch("pydis_site.apps.content.views.article_category.utils.get_article")
    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @patch("pydis_site.apps.content.views.article_category.utils.get_github_information")
    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_valid_category_article_code_200(
            self,
            gh_info_mock,
            get_category_mock,
            get_article_mock
    ):
        """Check that return code is 200 when visiting valid category article."""
        get_article_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("content:article_category", args=["category/test3"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_article_mock.assert_called_once()
        self.assertEqual(get_category_mock.call_count, 2)
        gh_info_mock.assert_called_once()

    @patch("pydis_site.apps.content.views.article_category.utils.get_article")
    @patch("pydis_site.apps.content.views.article_category.utils.get_category")
    @patch("pydis_site.apps.content.views.article_category.utils.get_github_information")
    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_invalid_category_article_code_404(
            self,
            gh_info_mock,
            get_category_mock,
            get_article_mock
    ):
        """Check that return code is 200 when trying to visit invalid category article."""
        get_article_mock.side_effect = Http404("Article not found.")

        url = reverse("content:article_category", args=["category/invalid"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_article_mock.assert_not_called()
        get_category_mock.assert_not_called()
        gh_info_mock.assert_not_called()

    @override_settings(ARTICLES_PATH=BASE_PATH)
    def test_article_category_template_names(self):
        """Check that this return category, article template or raise Http404."""
        factory = RequestFactory()
        cases = [
            {"location": "category", "output": ["content/listing.html"]},
            {"location": "test", "output": ["content/article.html"]},
            {"location": "invalid", "output": None, "raises": Http404}
        ]

        for case in cases:
            with self.subTest(location=case["location"], output=case["output"]):
                request = factory.get(f"/articles/{case['location']}")
                instance = ArticleOrCategoryView()
                instance.request = request
                instance.kwargs = {"location": case["location"]}

                if "raises" in case:
                    with self.assertRaises(case["raises"]):
                        instance.get_template_names()
                else:
                    self.assertEqual(case["output"], instance.get_template_names())
