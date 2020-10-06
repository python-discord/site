from unittest.mock import patch

from django.http import Http404
from django.test import TestCase
from django_hosts.resolvers import reverse


class TestArticlesIndexView(TestCase):
    @patch("pydis_site.apps.content.views.articles.get_articles")
    @patch("pydis_site.apps.content.views.articles.get_categories")
    def test_articles_index_return_200(self, get_categories_mock, get_articles_mock):
        """Check that content index return HTTP code 200."""
        get_categories_mock.return_value = {}
        get_articles_mock.return_value = {}

        url = reverse('articles:articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_articles_mock.assert_called_once()
        get_categories_mock.assert_called_once()


class TestArticleView(TestCase):
    @patch("pydis_site.apps.content.views.article.get_article")
    @patch("pydis_site.apps.content.views.article.get_category")
    def test_article_return_code_200(self, get_category_mock, get_article_mock):
        get_article_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("articles:article", args=["test-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_category_mock.assert_not_called()
        get_article_mock.assert_called_once_with("test-guide", None)

    @patch("pydis_site.apps.content.views.article.get_article")
    @patch("pydis_site.apps.content.views.article.get_category")
    def test_article_return_404(self, get_category_mock, get_article_mock):
        """Check that return code is 404 when invalid article provided."""
        get_article_mock.side_effect = Http404("Article not found.")

        url = reverse("articles:article", args=["invalid-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_article_mock.assert_called_once_with("invalid-guide", None)
        get_category_mock.assert_not_called()


class TestCategoryView(TestCase):
    @patch("pydis_site.apps.content.views.category.get_category")
    @patch("pydis_site.apps.content.views.category.get_articles")
    def test_valid_category_code_200(self, get_articles_mock, get_category_mock):
        """Check that return code is 200 when visiting valid category."""
        get_category_mock.return_value = {"name": "test", "description": "test"}
        get_articles_mock.return_value = {}

        url = reverse("articles:category", args=["category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        get_articles_mock.assert_called_once_with("category")
        get_category_mock.assert_called_once_with("category")

    @patch("pydis_site.apps.content.views.category.get_category")
    @patch("pydis_site.apps.content.views.category.get_articles")
    def test_invalid_category_code_404(self, get_articles_mock, get_category_mock):
        """Check that return code is 404 when trying to visit invalid category."""
        get_category_mock.side_effect = Http404("Category not found.")

        url = reverse("articles:category", args=["invalid-category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        get_category_mock.assert_called_once_with("invalid-category")
        get_articles_mock.assert_not_called()


class TestCategoryArticlesView(TestCase):
    @patch("pydis_site.apps.content.views.article.get_article")
    @patch("pydis_site.apps.content.views.article.get_category")
    def test_valid_category_article_code_200(self, get_category_mock, get_article_mock):
        """Check that return code is 200 when visiting valid category article."""
        get_article_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("articles:category_article", args=["category", "test3"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_article_mock.assert_called_once_with("test3", "category")
        get_category_mock.assert_called_once_with("category")

    @patch("pydis_site.apps.content.views.article.get_article")
    @patch("pydis_site.apps.content.views.article.get_category")
    def test_invalid_category_article_code_404(self, get_category_mock, get_article_mock):
        """Check that return code is 200 when trying to visit invalid category article."""
        get_article_mock.side_effect = Http404("Article not found.")

        url = reverse("articles:category_article", args=["category", "invalid"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_article_mock.assert_called_once_with("invalid", "category")
        get_category_mock.assert_not_called()
