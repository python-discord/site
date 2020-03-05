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
            'id': '602951077675139072',
            'channel_id': '291284109232308226',
            'delete_date': delete_at.isoformat()[:-1]
        }
        cases = (
            ('id', '-602951077675139072'),
            ('channel_id', '-291284109232308226')
        )

        for field, invalid_value in cases:
            with self.subTest(fied=field, invalid_value=invalid_value):
                test_data = data.copy()
                test_data.update({field: invalid_value})

                response = self.client.post(url, test_data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {
                    field: ['Ensure this value is greater than or equal to 0.']
                })


class ListTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        delete_at = datetime.datetime.now() + datetime.timedelta(days=1)
        aware_delete_at = delete_at.replace(tzinfo=datetime.timezone.utc)

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
        url = reverse('bot:offensivemessage-list', host='api')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), self.messages)


class DeletionTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
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

        self.assertFalse(
            OffensiveMessage.objects.filter(id=self.valid_offensive_message.id).exists()
        )


class NotAllowedMethodsTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        delete_at = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)

        cls.valid_offensive_message = OffensiveMessage.objects.create(
            id=602951077675139072,
            channel_id=291284109232308226,
            delete_date=delete_at.isoformat()
        )

    def test_returns_405_for_patch_and_put_requests(self):
        url = reverse(
            'bot:offensivemessage-detail', host='api', args=(self.valid_offensive_message.id,)
        )
        not_allowed_methods = (self.client.patch, self.client.put)

        for method in not_allowed_methods:
            with self.subTest(method=method):
                response = method(url, {})
                self.assertEqual(response.status_code, 405)
