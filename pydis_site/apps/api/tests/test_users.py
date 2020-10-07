from unittest.mock import patch

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Role, User
from ..models.bot.metricity import NotFound


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
    def setUpTestData(cls):
        cls.role = Role.objects.create(
            id=5,
            name="Test role pls ignore",
            colour=2,
            permissions=0b01010010101,
            position=1
        )

    def test_accepts_valid_data(self):
        url = reverse('bot:user-list', host='api')
        data = {
            'id': 42,
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
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.discriminator, data['discriminator'])
        self.assertEqual(user.in_guild, data['in_guild'])

    def test_supports_multi_creation(self):
        url = reverse('bot:user-list', host='api')
        data = [
            {
                'id': 5,
                'name': "test man",
                'discriminator': 42,
                'roles': [
                    self.role.id
                ],
                'in_guild': True
            },
            {
                'id': 8,
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
            'discriminator': "totally!"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)


class UserModelTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role_top = Role.objects.create(
            id=777,
            name="High test role",
            colour=2,
            permissions=0b01010010101,
            position=10,
        )
        cls.role_bottom = Role.objects.create(
            id=888,
            name="Low test role",
            colour=2,
            permissions=0b01010010101,
            position=1,
        )
        cls.developers_role = Role.objects.create(
            id=1234567,
            name="Developers",
            colour=1234,
            permissions=0b01010010101,
            position=2,
        )
        cls.user_with_roles = User.objects.create(
            id=1,
            name="Test User with two roles",
            discriminator=1,
            in_guild=True,
        )
        cls.user_with_roles.roles.extend([cls.role_bottom.id, cls.role_top.id])

        cls.user_without_roles = User.objects.create(
            id=2,
            name="Test User without roles",
            discriminator=2222,
            in_guild=True,
        )

    def test_correct_top_role_property_user_with_roles(self):
        """Tests if the top_role property returns the correct role."""
        top_role = self.user_with_roles.top_role
        self.assertIsInstance(top_role, Role)
        self.assertEqual(top_role.id, self.role_top.id)

    def test_correct_top_role_property_user_without_roles(self):
        """Tests if the top_role property returns the correct role."""
        top_role = self.user_without_roles.top_role
        self.assertIsInstance(top_role, Role)
        self.assertEqual(top_role.id, self.developers_role.id)

    def test_correct_username_formatting(self):
        """Tests the username property with both name and discriminator formatted together."""
        self.assertEqual(self.user_with_roles.username, "Test User with two roles#0001")


class UserMetricityTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id=0,
            name="Test user",
            discriminator=1,
            in_guild=True,
        )

    def test_get_metricity_data(self):
        # Given
        verified_at = "foo"
        total_messages = 1
        self.mock_metricity_user(verified_at, total_messages)

        # When
        url = reverse('bot:user-metricity-data', args=[0], host='api')
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "verified_at": verified_at,
            "total_messages": total_messages,
        })

    def test_no_metricity_user(self):
        # Given
        self.mock_no_metricity_user()

        # When
        url = reverse('bot:user-metricity-data', args=[0], host='api')
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def mock_metricity_user(self, verified_at, total_messages):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.return_value = dict(verified_at=verified_at)
        self.metricity.total_messages.return_value = total_messages

    def mock_no_metricity_user(self):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.side_effect = NotFound()
        self.metricity.total_messages.side_effect = NotFound()
