import os
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django_hosts.resolvers import reverse


class TestGuidesIndexView(TestCase):
    def test_guides_index_return_200(self):
        """Check that guides index return HTTP code 200."""
        url = reverse('guide:guides')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestGuideView(TestCase):
    def test_guide_return_code_200(self):
        """Check that return code is 200 when valid guide provided."""
        test_cases = (
            "test",
            "test2",
        )
        for case in test_cases:
            url = reverse("guide:guide", args=[case])
            join_return_value = os.path.join(
                settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", f"{case}.md"
            )
            with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
                p.return_value = join_return_value
                response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_guide_return_404(self):
        """Check that return code is 404 when invalid guide provided."""
        url = reverse("guide:guide", args=["invalid-guide"])
        join_return_value = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "invalid-guide.md"
        )
        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.return_value = join_return_value
            response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class TestCategoryView(TestCase):
    def test_valid_category_code_200(self):
        """Check that return code is 200 when visiting valid category."""
        url = reverse("guide:category", args=["category"])
        base = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "category"
        )
        join_return_value = [base, os.path.join(base, "_info.yml")]

        for filename in os.listdir(base):
            if filename.endswith(".md"):
                join_return_value.append(os.path.join(base, filename))

        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.side_effect = join_return_value
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_invalid_category_code_404(self):
        """Check that return code is 404 when trying to visit invalid category."""
        url = reverse("guide:category", args=["invalid-category"])
        join_return_value = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "invalid-category"
        )
        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.return_value = join_return_value
            response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class TestCategoryGuidesView(TestCase):
    def test_valid_category_guide_code_200(self):
        """Check that return code is 200 when visiting valid category article."""
        url = reverse("guide:category_guide", args=["category", "test3"])
        category_directory = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "category"
        )

        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.side_effect = (
                category_directory,
                os.path.join(category_directory, "test3.md"),
                os.path.join(category_directory, "_info.yml")
            )
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_invalid_category_guide_code_404(self):
        """Check that return code is 200 when trying to visit invalid category article."""
        url = reverse("guide:category_guide", args=["category", "invalid"])
        category_directory = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "category"
        )

        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.side_effect = (
                category_directory,
                os.path.join(category_directory, "invalid.md"),
                os.path.join(category_directory, "_info.yml")
            )
            response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_invalid_category_code_404(self):
        """Check that response code is 404 when provided category for article is incorrect."""
        url = reverse("guide:category_guide", args=["invalid", "guide"])
        category_directory = os.path.join(
            settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "invalid"
        )

        with patch("pydis_site.apps.guides.views.guide.os.path.join") as p:
            p.return_value = category_directory
            response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
