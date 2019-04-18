from django.conf import settings
from django.test import TestCase

from pydis_site.apps.main.models import RepositoryMetadata
from pydis_site.apps.main.views import HomeView


class TestRepositoryMetadataHelpers(TestCase):

    def test_returns_metadata(self):
        """Test if the _get_repo_data helper actually returns what it should."""

        home_view = HomeView()
        metadata = home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)
        self.assertEquals(len(metadata), len(settings.HOMEPAGE_REPOS))

    def test_returns_api_data(self):
        """Tests if the _get_api_data helper returns what it should."""

        home_view = HomeView()
        api_data = home_view._get_api_data()
        repo = settings.HOMEPAGE_REPOS[0]

        self.assertIsInstance(api_data, dict)
        self.assertEquals(len(api_data), len(settings.HOMEPAGE_REPOS))
        self.assertIn(repo, api_data.keys())
        self.assertIn("stargazers_count", api_data[repo])
