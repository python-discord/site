from django.test import TestCase
from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Member, Role


class UnauthedDocumentationLinkAPITests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('bot:member-detail', args=('whatever',), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('bot:member-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('bot:member-list', host='api')
        response = self.client.post(url, data={'hi': 'there'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('bot:member-detail', args=('whatever',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role = Role.objects.create(
            id=5,
            name="Test role pls ignore",
            colour=2,
            permissions=0b01010010101
        )

    def test_accepts_valid_data(self):
        url = reverse('bot:member-list', host='api')
        data = {
            'id': 42,
            'avatar_hash': "validavatarhashiswear",
            'name': "Test",
            'discriminator': 42,
            'roles': [
                self.role.id
            ]
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

        user = Member.objects.get(id=42)
        self.assertEqual(user.avatar_hash, data['avatar_hash'])
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.discriminator, data['discriminator'])

    def test_supports_multi_creation(self):
        url = reverse('bot:member-list', host='api')
        data = [
            {
                'id': 5,
                'avatar_hash': "hahayes",
                'name': "test man",
                'discriminator': 42,
                'roles': [
                    self.role.id
                ]
            },
            {
                'id': 8,
                'avatar_hash': "maybenot",
                'name': "another test man",
                'discriminator': 555,
                'roles': []
            }
        ]

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

    def test_returns_400_for_unknown_role_id(self):
        url = reverse('bot:member-list', host='api')
        data = {
            'id': 5,
            'avatar_hash': "hahayes",
            'name': "test man",
            'discriminator': 42,
            'roles': [
                190810291
            ]
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_bad_data(self):
        url = reverse('bot:member-list', host='api')
        data = {
            'id': True,
            'avatar_hash': 1902831,
            'discriminator': "totally!"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
