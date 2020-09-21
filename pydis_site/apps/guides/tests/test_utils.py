import os
from unittest.mock import patch

from django.conf import settings
from django.http import Http404
from django.test import TestCase

from pydis_site.apps.guides import utils


class TestGetCategory(TestCase):
    def test_get_category_successfully(self):
        """Check does this get right data from category data file."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "category")
        info_path = os.path.join(path, "_info.yml")
        with patch("pydis_site.apps.guides.utils.os.path.join") as p:
            p.side_effect = [path, info_path]
            result = utils.get_category("category")

        self.assertEqual(result, {"name": "My Category", "description": "My Description"})

    def test_get_category_not_exists(self):
        """Check does this raise 404 error when category don't exists."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "invalid")
        with patch("pydis_site.apps.guides.utils.os.path.join") as p:
            p.return_value = path
            with self.assertRaises(Http404):
                utils.get_category("invalid")

    def test_get_category_not_directory(self):
        """Check does this raise 404 error when category isn't directory."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides", "test.md")
        with patch("pydis_site.apps.guides.utils.os.path.join") as p:
            p.return_value = path
            with self.assertRaises(Http404):
                utils.get_category("test.md")


class TestGetCategories(TestCase):
    def test_get_categories(self):
        """Check does this return test guides categories."""
        path = os.path.join(settings.BASE_DIR, "pydis_site", "apps", "guides", "tests", "test_guides")

        side_effects = [path]
        for name in os.listdir(path):
            side_effects.append(os.path.join(path, name))
            if os.path.isdir(os.path.join(path, name)):
                side_effects.append(os.path.join(path, name))
                side_effects.append(os.path.join(path, name, "_info.yml"))

        with patch("pydis_site.apps.guides.utils.os.path.join") as p:
            p.side_effect = side_effects
            result = utils.get_categories()

        self.assertEqual(result, {"category": {"name": "My Category", "description": "My Description"}})
