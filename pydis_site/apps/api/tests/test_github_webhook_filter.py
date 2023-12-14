from unittest import mock
from urllib.error import HTTPError

from django.urls import reverse
from rest_framework.test import APITestCase

from pydis_site.apps.api.views import GitHubWebhookFilterView

class GitHubWebhookFilterAPITests(APITestCase):
    def test_ignores_bot_sender(self):
        url = reverse('api:github-webhook-filter', args=('id', 'token'))
        payload = {'sender': {'login': 'limette', 'type': 'bot'}}
        headers = {'X-GitHub-Event': 'pull_request_review'}
        response = self.client.post(url, data=payload, headers=headers)
        self.assertEqual(response.status_code, 203)

    def test_accepts_interesting_events(self):
        url = reverse('api:github-webhook-filter', args=('id', 'token'))
        payload = {
            'ref': 'refs/heads/master',
            'pull_request': {
                'user': {
                    'login': "lemon",
                }
            },
            'review': {
                'state': 'commented',
                'body': "Amazing!!!"
            },
            'repository': {
                'name': 'black',
                'owner': {
                    'login': 'psf',
                }
            }
        }
        headers = {'X-GitHub-Event': 'pull_request_review'}

        with mock.patch('urllib.request.urlopen') as urlopen:
            urlopen.return_value = mock.MagicMock()
            context_mock = urlopen.return_value.__enter__.return_value
            context_mock.status = 299
            context_mock.getheaders.return_value = [('X-Clacks-Overhead', 'Joe Armstrong')]
            context_mock.read.return_value = b'{"status": "ok"}'

            response = self.client.post(url, data=payload, headers=headers)
            self.assertEqual(response.status_code, context_mock.status)
            self.assertEqual(response.headers.get('X-Clacks-Overhead'), 'Joe Armstrong')

    def test_rate_limit_is_logged_to_sentry(self):
        url = reverse('api:github-webhook-filter', args=('id', 'token'))
        payload = {}
        headers = {'X-GitHub-Event': 'pull_request_review'}
        with (
            mock.patch('urllib.request.urlopen') as urlopen,
            mock.patch.object(GitHubWebhookFilterView, "logger") as logger,
        ):
            urlopen.side_effect = HTTPError(None, 429, 'Too Many Requests', {}, None)
            logger.warning = mock.PropertyMock()
            self.client.post(url, data=payload, headers=headers)

            logger.warning.assert_called_once()
