import datetime

from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import OffensiveMessage


def create_offensive_message() -> OffensiveMessage:
    """Creates and returns an `OffensiveMessgage` record for tests."""
    delete_at = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=1)

    return OffensiveMessage.objects.create(
        id=602951077675139072,
        channel_id=291284109232308226,
        delete_date=delete_at,
    )


class CreationTests(AuthenticatedAPITestCase):
    def test_accept_valid_data(self):
        url = reverse('api:bot:offensivemessage-list')
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)  # noqa: DTZ005
        data = {
            'id': '602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }

        aware_delete_at = delete_at.replace(tzinfo=datetime.UTC)

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        offensive_message = OffensiveMessage.objects.get(id=response.json()['id'])
        self.assertAlmostEqual(
            aware_delete_at,
            offensive_message.delete_date,
            delta=datetime.timedelta(seconds=1)
        )
        self.assertEqual(data['id'], str(offensive_message.id))
        self.assertEqual(data['channel_id'], str(offensive_message.channel_id))

    def test_returns_400_on_non_future_date(self):
        url = reverse('api:bot:offensivemessage-list')
        delete_at = datetime.datetime.now() - datetime.timedelta(days=1)  # noqa: DTZ005
        data = {
            'id': '602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'delete_date': ['Date must be a future date']
        })

    def test_returns_400_on_negative_id_or_channel_id(self):
        url = reverse('api:bot:offensivemessage-list')
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)  # noqa: DTZ005
        data = {
            'id': '602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }
        cases = (
            ('id', '-602951077675139072'),
            ('channel_id', '-291284109232308226')
        )

        for field, invalid_value in cases:
            with self.subTest(field=field, invalid_value=invalid_value):
                test_data = data.copy()
                test_data.update({field: invalid_value})

                response = self.client.post(url, test_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {
                    field: ['Ensure this value is greater than or equal to 0.']
                })


class ListTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)  # noqa: DTZ005
        aware_delete_at = delete_at.replace(tzinfo=datetime.UTC)

        cls.messages = [
            {
                'id': 602951077675139072,
                'channel_id': 91284109232308226,
            },
            {
                'id': 645298201494159401,
                'channel_id': 592000283102674944
            }
        ]

        cls.of1 = OffensiveMessage.objects.create(
            **cls.messages[0],
            delete_date=aware_delete_at.isoformat()
        )
        cls.of2 = OffensiveMessage.objects.create(
            **cls.messages[1],
            delete_date=aware_delete_at.isoformat()
        )

        # Expected API answer :
        cls.messages[0]['delete_date'] = delete_at.isoformat() + 'Z'
        cls.messages[1]['delete_date'] = delete_at.isoformat() + 'Z'

    def test_get_data(self):
        url = reverse('api:bot:offensivemessage-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), self.messages)


class DeletionTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_offensive_message = create_offensive_message()

    def test_delete_data(self):
        url = reverse(
            'api:bot:offensivemessage-detail', args=(self.valid_offensive_message.id,)
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            OffensiveMessage.objects.filter(id=self.valid_offensive_message.id).exists()
        )


class UpdateOffensiveMessageTestCase(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.message = create_offensive_message()
        cls.in_one_week = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=7)

    def test_updating_message(self):
        url = reverse('api:bot:offensivemessage-detail', args=(self.message.id,))
        data = {'delete_date': self.in_one_week.isoformat()}
        update_response = self.client.patch(url, data=data)
        self.assertEqual(update_response.status_code, 200)

        self.message.refresh_from_db()
        self.assertAlmostEqual(
            self.message.delete_date,
            self.in_one_week,
            delta=datetime.timedelta(seconds=1),
        )

    def test_updating_nonexistent_message(self):
        url = reverse('api:bot:offensivemessage-detail', args=(self.message.id + 1,))
        data = {'delete_date': self.in_one_week}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 404)
        self.message.refresh_from_db()
        self.assertNotAlmostEqual(
            self.message.delete_date,
            self.in_one_week,
            delta=datetime.timedelta(seconds=1),
        )


class NotAllowedMethodsTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.message = create_offensive_message()

    def test_returns_405_for_get(self):
        url = reverse('api:bot:offensivemessage-detail', args=(self.message.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
