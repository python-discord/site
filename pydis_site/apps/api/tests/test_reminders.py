from datetime import datetime

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import User


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


class ReminderCreationTests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.author = User.objects.create(
            id=1234,
            name='Mermaid Man',
            discriminator=1234,
            avatar_hash=None,
        )
        self.data = {
            'author': self.author.id,
            'content': 'Remember to...wait what was it again?',
            'expiration': datetime.utcnow().isoformat(),
            'jump_url': "https://www.google.com",
            'channel_id': 123,
        }
        url = reverse('bot:reminder-list', host='api')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 201)

    def test_reminder_in_full_list(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.data['expiration'] += 'Z'  # Massaging a quirk of the response time format
        self.data['active'] = True
        self.data['id'] = 1
        self.assertEqual(response.json(), [self.data])
