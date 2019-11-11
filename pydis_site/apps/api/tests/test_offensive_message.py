import datetime

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import OffensiveMessage


class CreationTests(APISubdomainTestCase):
    def test_accept_valid_data(self):
        url = reverse('bot:offensivemessage-list', host='api')
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)
        data = {
            'id': '602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }

        aware_delete_at = delete_at.replace(tzinfo=datetime.timezone.utc)

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
        url = reverse('bot:offensivemessage-list', host='api')
        delete_at = datetime.datetime.now() - datetime.timedelta(days=1)
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
        url = reverse('bot:offensivemessage-list', host='api')
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)
        data = {
            'id': '-602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'id': ['Ensure this value is greater than or equal to 0.']
        })

        data = {
            'id': '602951077675139072',
            'channel_id': '-291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'channel_id': ['Ensure this value is greater than or equal to 0.']
        })


class DeletionTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        delete_at = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)

        cls.valid_offensive_message = OffensiveMessage.objects.create(
            id=602951077675139072,
            channel_id=291284109232308226,
            delete_date=delete_at.isoformat()
        )

    def test_delete_data(self):
        url = reverse(
            'bot:offensivemessage-detail', host='api', args=(self.valid_offensive_message.id,)
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        url = reverse('bot:offensivemessage-list', host='api')
        response = self.client.get(url)
        self.assertNotIn(self.valid_offensive_message.id, response.json())


class NotAllowedMethodsTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)

        cls.valid_offensive_message = OffensiveMessage.objects.create(
            id=602951077675139072,
            channel_id=291284109232308226,
            delete_date=delete_at.isoformat()[:-1]
        )

    def test_returns_405_for_patch_and_put_requests(self):
        url = reverse(
            'bot:offensivemessage-detail', host='api', args=(self.valid_offensive_message.id,)
        )

        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 405)
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, 405)
