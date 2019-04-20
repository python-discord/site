import json
from datetime import timedelta
from pathlib import Path
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from pydis_site.apps.home.models import RepositoryMetadata
from pydis_site.apps.home.views import HomeView


def mocked_requests_get(*args, **kwargs) -> "MockResponse":  # noqa
    """A mock version of requests.get, so we don't need to call the API every time we run a test"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == HomeView.github_api:
        json_path = Path(__file__).resolve().parent / "mock_github_api_response.json"
        with open(json_path, 'r') as json_file:
            mock_data = json.load(json_file)

        return MockResponse(mock_data, 200)

    return MockResponse(None, 404)


class TestRepositoryMetadataHelpers(TestCase):

    def setUp(self):
        """Executed before each test method."""

        self.home_view = HomeView()

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_returns_metadata(self, _: mock.MagicMock):
        """Test if the _get_repo_data helper actually returns what it should."""

        metadata = self.home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)
        self.assertEquals(len(metadata), len(self.home_view.repos))

    def test_returns_cached_metadata(self):
        """Test if the _get_repo_data helper returns cached data when available."""

        repo_data = RepositoryMetadata(
            repo_name="python-discord/site",
            description="testrepo",
            forks=42,
            stargazers=42,
            language="English",
        )
        repo_data.save()
        metadata = self.home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)
        self.assertIsInstance(str(metadata[0]), str)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_refresh_stale_metadata(self, _: mock.MagicMock):
        """Test if the _get_repo_data helper will refresh when the data is stale"""

        repo_data = RepositoryMetadata(
            repo_name="python-discord/site",
            description="testrepo",
            forks=42,
            stargazers=42,
            language="English",
            last_updated=timezone.now() - timedelta(seconds=HomeView.repository_cache_ttl + 1),
        )
        repo_data.save()
        metadata = self.home_view._get_repo_data()

        self.assertIsInstance(metadata[0], RepositoryMetadata)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_returns_api_data(self, _: mock.MagicMock):
        """Tests if the _get_api_data helper returns what it should."""

        api_data = self.home_view._get_api_data()
        repo = self.home_view.repos[0]

        self.assertIsInstance(api_data, dict)
        self.assertEquals(len(api_data), len(self.home_view.repos))
        self.assertIn(repo, api_data.keys())
        self.assertIn("stargazers_count", api_data[repo])

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_mocked_requests_get(self, mock_get: mock.MagicMock):
        """Tests if our mocked_requests_get is returning what it should."""

        success_data = mock_get(HomeView.github_api)
        fail_data = mock_get("failtest")

        self.assertEqual(success_data.status_code, 200)
        self.assertEqual(fail_data.status_code, 404)

        self.assertIsNotNone(success_data.json_data)
        self.assertIsNone(fail_data.json_data)
