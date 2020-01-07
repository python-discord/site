from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase


class UnauthedReminderAPITests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_list_returns_401(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.post(url, data={'not': 'important'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('bot:reminder-detail', args=('1234',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseReminderAPITests(APISubdomainTestCase):
    def test_list_all_returns_empty_list(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_delete_returns_404(self):
        url = reverse('bot:reminder-detail', args=('1234',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
