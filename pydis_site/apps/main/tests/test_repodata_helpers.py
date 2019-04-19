from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from pydis_site.apps.main.models import RepositoryMetadata
from pydis_site.apps.main.views import HomeView


class TestRepositoryMetadataHelpers(TestCase):

    def test_returns_metadata(self):
        """Test if the _get_repo_data helper actually returns what it should."""

        home_view = HomeView()
        metadata = home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)
        self.assertEquals(len(metadata), len(settings.HOMEPAGE_REPOS))

    def test_returns_cached_metadata(self):
        """Test if the _get_repo_data helper returns cached data when available."""

        home_view = HomeView()
        repo_data = RepositoryMetadata(
            repo_name="python-discord/site",
            description="testrepo",
            forks=42,
            stargazers=42,
            language="English",
        )
        repo_data.save()
        metadata = home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)
        print(metadata[0])  # Tests the __str__ in the model

    def test_refresh_stale_metadata(self):
        """Test if the _get_repo_data helper will refresh when the data is stale"""

        home_view = HomeView()
        repo_data = RepositoryMetadata(
            repo_name="python-discord/site",
            description="testrepo",
            forks=42,
            stargazers=42,
            language="English",
            last_updated=timezone.now() - timedelta(seconds=121),  # Make the data 2 minutes old.
        )
        repo_data.save()
        metadata = home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)

    def test_returns_api_data(self):
        """Tests if the _get_api_data helper returns what it should."""

        home_view = HomeView()
        api_data = home_view._get_api_data()
        repo = settings.HOMEPAGE_REPOS[0]

        self.assertIsInstance(api_data, dict)
        self.assertEquals(len(api_data), len(settings.HOMEPAGE_REPOS))
        self.assertIn(repo, api_data.keys())
        self.assertIn("stargazers_count", api_data[repo])
