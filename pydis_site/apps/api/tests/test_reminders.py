from datetime import datetime, timezone

from django.forms.models import model_to_dict
from django.urls import reverse

from .base import AuthenticatedAPITestCase
from ..models import Reminder, User


class UnauthedReminderAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_list_returns_401(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.post(url, data={'not': 'important'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('api:bot:reminder-detail', args=('1234',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class EmptyDatabaseReminderAPITests(AuthenticatedAPITestCase):
    def test_list_all_returns_empty_list(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_delete_returns_404(self):
        url = reverse('api:bot:reminder-detail', args=('1234',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)


class ReminderCreationTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=1234,
            name='Mermaid Man',
            discriminator=1234,
        )

    def test_accepts_valid_data(self):
        data = {
            'author': self.author.id,
            'content': 'Remember to...wait what was it again?',
            'expiration': datetime.utcnow().isoformat(),
            'jump_url': "https://www.google.com",
            'channel_id': 123,
            'mentions': [8888, 9999],
        }
        url = reverse('api:bot:reminder-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Reminder.objects.filter(id=1).first())

    def test_rejects_invalid_data(self):
        data = {
            'author': self.author.id,  # Missing multiple required fields
        }
        url = reverse('api:bot:reminder-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertRaises(Reminder.DoesNotExist, Reminder.objects.get, id=1)


class ReminderDeletionTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=6789,
            name='Barnacle Boy',
            discriminator=6789,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="Don't forget to set yourself a reminder",
            expiration=datetime.now(timezone.utc),
            jump_url="https://www.decliningmentalfaculties.com",
            channel_id=123
        )

    def test_delete_unknown_reminder_returns_404(self):
        url = reverse('api:bot:reminder-detail', args=('something',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_known_reminder_returns_204(self):
        url = reverse('api:bot:reminder-detail', args=(self.reminder.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertRaises(Reminder.DoesNotExist, Reminder.objects.get, id=self.reminder.id)


class ReminderListTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=6789,
            name='Patrick Star',
            discriminator=6789,
        )

        cls.reminder_one = Reminder.objects.create(
            author=cls.author,
            content="We should take Bikini Bottom, and push it somewhere else!",
            expiration=datetime.now(timezone.utc),
            jump_url="https://www.icantseemyforehead.com",
            channel_id=123
        )

        cls.reminder_two = Reminder.objects.create(
            author=cls.author,
            content="Gahhh-I love being purple!",
            expiration=datetime.now(timezone.utc),
            jump_url="https://www.goofygoobersicecreampartyboat.com",
            channel_id=123,
            active=False
        )

        drf_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        cls.rem_dict_one = model_to_dict(cls.reminder_one)
        cls.rem_dict_one['expiration'] = cls.rem_dict_one['expiration'].strftime(drf_format)
        cls.rem_dict_two = model_to_dict(cls.reminder_two)
        cls.rem_dict_two['expiration'] = cls.rem_dict_two['expiration'].strftime(drf_format)

    def test_reminders_in_full_list(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json(), [self.rem_dict_one, self.rem_dict_two])

    def test_filter_search(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.get(f'{url}?search={self.author.name}')

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json(), [self.rem_dict_one, self.rem_dict_two])

    def test_filter_field(self):
        url = reverse('api:bot:reminder-list')
        response = self.client.get(f'{url}?active=true')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.rem_dict_one])


class ReminderRetrieveTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=6789,
            name='Reminder author',
            discriminator=6789,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="Reminder content",
            expiration=datetime.now(timezone.utc),
            jump_url="http://example.com/",
            channel_id=123
        )

    def test_retrieve_unknown_returns_404(self):
        url = reverse('api:bot:reminder-detail', args=("not_an_id",))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_known_returns_200(self):
        url = reverse('api:bot:reminder-detail', args=(self.reminder.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ReminderUpdateTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            id=666,
            name='Man Ray',
            discriminator=666,
        )

        cls.reminder = Reminder.objects.create(
            author=cls.author,
            content="Squash those do-gooders",
            expiration=datetime.now(timezone.utc),
            jump_url="https://www.decliningmentalfaculties.com",
            channel_id=123
        )

        cls.data = {'content': 'Oops I forgot'}

    def test_patch_updates_record(self):
        url = reverse('api:bot:reminder-detail', args=(self.reminder.id,))
        response = self.client.patch(url, data=self.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Reminder.objects.filter(id=self.reminder.id).first().content,
            self.data['content']
        )
