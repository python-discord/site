from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django_hosts.resolvers import reverse

from pydis_site.apps.content.views import PageOrCategoryView

BASE_PATH = Path(settings.BASE_DIR, "pydis_site", "apps", "content", "tests", "test_content")


class TestPageOrCategoryView(TestCase):
    @override_settings(PAGES_PATH=BASE_PATH)
    @patch("pydis_site.apps.content.views.page_category.utils.get_page")
    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    def test_page_return_code_200(self, get_category_mock, get_page_mock):
        get_page_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("content:page_category", args=["test2"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_category_mock.assert_called_once()
        get_page_mock.assert_called_once()

    @patch("pydis_site.apps.content.views.page_category.utils.get_page")
    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_page_return_404(self, get_category_mock, get_page_mock):
        """Check that return code is 404 when invalid page provided."""
        get_page_mock.side_effect = Http404("Page not found.")

        url = reverse("content:page_category", args=["invalid-guide"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_page_mock.assert_not_called()
        get_category_mock.assert_not_called()

    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    @patch("pydis_site.apps.content.views.page_category.utils.get_pages")
    @patch("pydis_site.apps.content.views.page_category.utils.get_categories")
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_valid_category_code_200(
            self,
            get_categories_mock,
            get_pages_mock,
            get_category_mock
    ):
        """Check that return code is 200 when visiting valid category."""
        get_category_mock.return_value = {"name": "test", "description": "test"}
        get_pages_mock.return_value = {}

        url = reverse("content:page_category", args=["category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        get_pages_mock.assert_called_once()
        self.assertEqual(get_category_mock.call_count, 2)
        get_categories_mock.assert_called_once()

    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    @patch("pydis_site.apps.content.views.page_category.utils.get_pages")
    @patch("pydis_site.apps.content.views.page_category.utils.get_categories")
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_invalid_category_code_404(
            self,
            get_categories_mock,
            get_pages_mock,
            get_category_mock
    ):
        """Check that return code is 404 when trying to visit invalid category."""
        get_category_mock.side_effect = Http404("Category not found.")

        url = reverse("content:page_category", args=["invalid-category"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        get_category_mock.assert_not_called()
        get_pages_mock.assert_not_called()
        get_categories_mock.assert_not_called()

    @patch("pydis_site.apps.content.views.page_category.utils.get_page")
    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_valid_category_page_code_200(
            self,
            get_category_mock,
            get_page_mock
    ):
        """Check that return code is 200 when visiting valid category page."""
        get_page_mock.return_value = {"guide": "test", "metadata": {}}

        url = reverse("content:page_category", args=["category/test3"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_page_mock.assert_called_once()
        self.assertEqual(get_category_mock.call_count, 2)

    @patch("pydis_site.apps.content.views.page_category.utils.get_page")
    @patch("pydis_site.apps.content.views.page_category.utils.get_category")
    @override_settings(PAGES_PATH=BASE_PATH)
    def test_invalid_category_page_code_404(
            self,
            get_category_mock,
            get_page_mock
    ):
        """Check that return code is 200 when trying to visit invalid category page."""
        get_page_mock.side_effect = Http404("Page not found.")

        url = reverse("content:page_category", args=["category/invalid"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        get_page_mock.assert_not_called()
        get_category_mock.assert_not_called()

    @override_settings(PAGES_PATH=BASE_PATH)
    def test_page_category_template_names(self):
        """Check that this return category, page template or raise Http404."""
        factory = RequestFactory()
        cases = [
            {"location": "category", "output": ["content/listing.html"]},
            {"location": "test", "output": ["content/page.html"]},
            {"location": "invalid", "output": None, "raises": Http404}
        ]

        for case in cases:
            with self.subTest(location=case["location"], output=case["output"]):
                request = factory.get(f"/pages/{case['location']}")
                instance = PageOrCategoryView()
                instance.request = request
                location = Path(case["location"])
                instance.location = location
                instance.full_location = BASE_PATH / location

                if "raises" in case:
                    with self.assertRaises(case["raises"]):
                        instance.get_template_names()
                else:
                    self.assertEqual(case["output"], instance.get_template_names())
