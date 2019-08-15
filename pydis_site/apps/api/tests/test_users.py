from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Role, User


class UnauthedUserAPITests(APISubdomainTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('bot:user-detail', args=('whatever',), host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('bot:user-list', host='api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('bot:user-list', host='api')
        response = self.client.post(url, data={'hi': 'there'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('bot:user-detail', args=('whatever',), host='api')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):  # noqa
        cls.role = Role.objects.create(
            id=5,
            name="Test role pls ignore",
            colour=2,
            permissions=0b01010010101,
            position=1
        )
        cls.role_bottom = Role.objects.create(
            id=6,
            name="Low test role",
            colour=2,
            permissions=0b01010010101,
            position=0,
        )
        cls.role_top = Role.objects.create(
            id=7,
            name="High test role",
            colour=2,
            permissions=0b01010010101,
            position=10,
        )
        cls.role_test_user = User.objects.create(
            id=1,
            avatar_hash="coolavatarhash",
            name="Test User",
            discriminator=1111,
            in_guild=True,
        )
        cls.role_test_user.roles.add(cls.role_bottom, cls.role_top)

    def test_accepts_valid_data(self):
        url = reverse('bot:user-list', host='api')
        data = {
            'id': 42,
            'avatar_hash': "validavatarhashiswear",
            'name': "Test",
            'discriminator': 42,
            'roles': [
                self.role.id
            ],
            'in_guild': True
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

        user = User.objects.get(id=42)
        self.assertEqual(user.avatar_hash, data['avatar_hash'])
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.discriminator, data['discriminator'])
        self.assertEqual(user.in_guild, data['in_guild'])

    def test_supports_multi_creation(self):
        url = reverse('bot:user-list', host='api')
        data = [
            {
                'id': 5,
                'avatar_hash': "hahayes",
                'name': "test man",
                'discriminator': 42,
                'roles': [
                    self.role.id
                ],
                'in_guild': True
            },
            {
                'id': 8,
                'avatar_hash': "maybenot",
                'name': "another test man",
                'discriminator': 555,
                'roles': [],
                'in_guild': False
            }
        ]

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

    def test_returns_400_for_unknown_role_id(self):
        url = reverse('bot:user-list', host='api')
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
        url = reverse('bot:user-list', host='api')
        data = {
            'id': True,
            'avatar_hash': 1902831,
            'discriminator': "totally!"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_correct_top_role_property(self):
        """Tests if the top_role property returns the correct role."""
        top_role = self.role_test_user.top_role
        self.assertIsInstance(top_role, Role)
        self.assertEqual(top_role.id, self.role_top.id)
