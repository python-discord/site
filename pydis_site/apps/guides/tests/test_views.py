from unittest.mock import patch

from django.http import Http404
from django.test import TestCase
from django_hosts.resolvers import reverse


class TestGuidesIndexView(TestCase):
    @patch("pydis_site.apps.guides.views.guides.get_guides")
    @patch("pydis_site.apps.guides.views.guides.get_categories")
    def test_guides_index_return_200(self, get_categories_mock, get_guides_mock):
        """Check that guides index return HTTP code 200."""
        get_categories_mock.return_value = {}
        get_guides_mock.return_value = {}

        url = reverse('guide:guides')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_guides_mock.assert_called_once()
        get_categories_mock.assert_called_once()


class TestGuideView(TestCase):
    @patch("pydis_site.apps.guides.views.guide.os.path.getmtime")
    @patch("pydis_site.apps.guides.views.guide.get_guide")
    @patch("pydis_site.apps.guides.views.guide.get_category")
    def test_guide_return_code_200(self, get_category_mock, get_guide_mock, get_time_mock):
        get_guide_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("guide:guide", args=["test-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_category_mock.assert_not_called()
        get_guide_mock.assert_called_once_with("test-guide", None)

    @patch("pydis_site.apps.guides.views.guide.os.path.getmtime")
    @patch("pydis_site.apps.guides.views.guide.get_guide")
    @patch("pydis_site.apps.guides.views.guide.get_category")
    def test_guide_return_404(self, get_category_mock, get_guide_mock, get_time_mock):
        """Check that return code is 404 when invalid guide provided."""
        get_guide_mock.side_effect = Http404("Guide not found.")

        url = reverse("guide:guide", args=["invalid-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_guide_mock.assert_called_once_with("invalid-guide", None)
        get_category_mock.assert_not_called()


class TestCategoryView(TestCase):
    @patch("pydis_site.apps.guides.views.category.get_category")
    @patch("pydis_site.apps.guides.views.category.get_guides")
    def test_valid_category_code_200(self, get_guides_mock, get_category_mock):
        """Check that return code is 200 when visiting valid category."""
        get_category_mock.return_value = {"name": "test", "description": "test"}
        get_guides_mock.return_value = {}

        url = reverse("guide:category", args=["category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        get_guides_mock.assert_called_once_with("category")
        get_category_mock.assert_called_once_with("category")

    @patch("pydis_site.apps.guides.views.category.get_category")
    @patch("pydis_site.apps.guides.views.category.get_guides")
    def test_invalid_category_code_404(self, get_guides_mock, get_category_mock):
        """Check that return code is 404 when trying to visit invalid category."""
        get_category_mock.side_effect = Http404("Category not found.")

        url = reverse("guide:category", args=["invalid-category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        get_category_mock.assert_called_once_with("invalid-category")
        get_guides_mock.assert_not_called()


class TestCategoryGuidesView(TestCase):
    @patch("pydis_site.apps.guides.views.guide.os.path.getmtime")
    @patch("pydis_site.apps.guides.views.guide.get_guide")
    @patch("pydis_site.apps.guides.views.guide.get_category")
    def test_valid_category_guide_code_200(self, get_category_mock, get_guide_mock, get_time_mock):
        """Check that return code is 200 when visiting valid category article."""
        get_guide_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("guide:category_guide", args=["category", "test3"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_guide_mock.assert_called_once_with("test3", "category")
        get_category_mock.assert_called_once_with("category")

    @patch("pydis_site.apps.guides.views.guide.os.path.getmtime")
    @patch("pydis_site.apps.guides.views.guide.get_guide")
    @patch("pydis_site.apps.guides.views.guide.get_category")
    def test_invalid_category_guide_code_404(self, get_category_mock, get_guide_mock, get_time_mock):
        """Check that return code is 200 when trying to visit invalid category article."""
        get_guide_mock.side_effect = Http404("Guide not found.")

        url = reverse("guide:category_guide", args=["category", "invalid"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_guide_mock.assert_called_once_with("invalid", "category")
        get_category_mock.assert_not_called()
