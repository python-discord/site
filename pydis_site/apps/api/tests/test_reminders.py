from datetime import datetime

from django.forms.models import model_to_dict
from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Reminder, User


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
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=1234,
            name='Mermaid Man',
            discriminator=1234,
            avatar_hash=None,
        )

    def test_accepts_valid_data(self):
        data = {
            'author': self.author.id,
            'content': 'Remember to...wait what was it again?',
            'expiration': datetime.utcnow().isoformat(),
            'jump_url': "https://www.google.com",
            'channel_id': 123,
        }
        url = reverse('bot:reminder-list', host='api')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Reminder.objects.get(id=1))

    def test_rejects_invalid_data(self):
        data = {
            'author': self.author.id,  # Missing multiple required fields
        }
        url = reverse('bot:reminder-list', host='api')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertRaises(Reminder.DoesNotExist, Reminder.objects.get, id=1)


class ReminderDeletionTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=6789,
            name='Barnacle Boy',
            discriminator=6789,
            avatar_hash=None,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="Don't forget to set yourself a reminder",
            expiration=datetime.utcnow().isoformat(),
            jump_url="https://www.decliningmentalfaculties.com",
            channel_id=123
        )

    def test_delete_unknown_reminder_returns_404(self):
        url = reverse('bot:reminder-detail', args=('something',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_known_reminder_returns_204(self):
        url = reverse('bot:reminder-detail', args=(self.reminder.id,), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertRaises(Reminder.DoesNotExist, Reminder.objects.get, id=self.reminder.id)


class ReminderListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=6789,
            name='Patrick Star',
            discriminator=6789,
            avatar_hash=None,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="We should take Bikini Bottom, and push it somewhere else!",
            expiration=datetime.utcnow().isoformat(),
            jump_url="https://www.icantseemyforehead.com",
            channel_id=123
        )

        cls.rem_dict = model_to_dict(cls.reminder)
        cls.rem_dict['expiration'] += 'Z'  # Massaging a quirk of the response time format

    def test_reminder_in_full_list(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.rem_dict])

    def test_filter_search(self):
        url = reverse('bot:reminder-list', host='api')
        response = self.client.get(f'{url}?search={self.author.name}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.rem_dict])


class ReminderUpdateTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=666,
            name='Man Ray',
            discriminator=666,
            avatar_hash=None,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="Squash those do-gooders",
            expiration=datetime.utcnow().isoformat(),
            jump_url="https://www.decliningmentalfaculties.com",
            channel_id=123
        )

        cls.data = {'content': 'Oops I forgot'}

    def test_patch_updates_record(self):
        url = reverse('bot:reminder-detail', args=(self.reminder.id,), host='api')
        response = self.client.patch(url, data=self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reminder.objects.get(id=self.reminder.id).content, self.data['content'])
