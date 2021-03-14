from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
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

        cls.user = User.objects.create(
            id=11,
            name="Name doesn't matter.",
            discriminator=1122,
            in_guild=True
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
        self.assertEqual(response.json(), [])

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

    def test_returns_400_for_user_recreation(self):
        """Return 201 if User is already present in database as it skips User creation."""
        url = reverse('bot:user-list', host='api')
        data = [{
            'id': 11,
            'name': 'You saw nothing.',
            'discriminator': 112,
            'in_guild': True
        }]
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_returns_400_for_duplicate_request_users(self):
        """Return 400 if 2 Users with same ID is passed in the request data."""
        url = reverse('bot:user-list', host='api')
        data = [
            {
                'id': 11,
                'name': 'You saw nothing.',
                'discriminator': 112,
                'in_guild': True
            },
            {
                'id': 11,
                'name': 'You saw nothing part 2.',
                'discriminator': 1122,
                'in_guild': False
            }
        ]
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_existing_user(self):
        """Returns 400 if user is already present in DB."""
        url = reverse('bot:user-list', host='api')
        data = {
            'id': 11,
            'name': 'You saw nothing part 3.',
            'discriminator': 1122,
            'in_guild': True
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)


class MultiPatchTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role_developer = Role.objects.create(
            id=159,
            name="Developer",
            colour=2,
            permissions=0b01010010101,
            position=10,
        )
        cls.user_1 = User.objects.create(
            id=1,
            name="Patch test user 1.",
            discriminator=1111,
            in_guild=True
        )
        cls.user_2 = User.objects.create(
            id=2,
            name="Patch test user 2.",
            discriminator=2222,
            in_guild=True
        )

    def test_multiple_users_patch(self):
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                "id": 1,
                "name": "User 1 patched!",
                "discriminator": 1010,
                "roles": [self.role_developer.id],
                "in_guild": False
            },
            {
                "id": 2,
                "name": "User 2 patched!"
            }
        ]

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], data[0])

        user_2 = User.objects.get(id=2)
        self.assertEqual(user_2.name, data[1]["name"])

    def test_returns_400_for_missing_user_id(self):
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                "name": "I am ghost user!",
                "discriminator": 1010,
                "roles": [self.role_developer.id],
                "in_guild": False
            },
            {
                "name": "patch me? whats my id?"
            }
        ]
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_404_for_not_found_user(self):
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                "id": 1,
                "name": "User 1 patched again!!!",
                "discriminator": 1010,
                "roles": [self.role_developer.id],
                "in_guild": False
            },
            {
                "id": 22503405,
                "name": "User unknown not patched!"
            }
        ]
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_returns_400_for_bad_data(self):
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                "id": 1,
                "in_guild": "Catch me!"
            },
            {
                "id": 2,
                "discriminator": "find me!"
            }
        ]

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_insufficient_data(self):
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                "id": 1,
            },
            {
                "id": 2,
            }
        ]
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_duplicate_request_users(self):
        """Return 400 if 2 Users with same ID is passed in the request data."""
        url = reverse("bot:user-bulk-patch", host="api")
        data = [
            {
                'id': 1,
                'name': 'You saw nothing.',
            },
            {
                'id': 1,
                'name': 'You saw nothing part 2.',
            }
        ]
        response = self.client.patch(url, data=data)
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


class UserPaginatorTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        users = []
        for i in range(1, 10_001):
            users.append(User(
                id=i,
                name=f"user{i}",
                discriminator=1111,
                in_guild=True
            ))
        cls.users = User.objects.bulk_create(users)

    def test_returns_single_page_response(self):
        url = reverse("bot:user-list", host="api")
        response = self.client.get(url).json()
        self.assertIsNone(response["next_page_no"])
        self.assertIsNone(response["previous_page_no"])

    def test_returns_next_page_number(self):
        User.objects.create(
            id=10_001,
            name="user10001",
            discriminator=1111,
            in_guild=True
        )
        url = reverse("bot:user-list", host="api")
        response = self.client.get(url).json()
        self.assertEqual(2, response["next_page_no"])

    def test_returns_previous_page_number(self):
        User.objects.create(
            id=10_001,
            name="user10001",
            discriminator=1111,
            in_guild=True
        )
        url = reverse("bot:user-list", host="api")
        response = self.client.get(url, {"page": 2}).json()
        self.assertEqual(1, response["previous_page_no"])


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
        joined_at = "foo"
        total_messages = 1
        total_blocks = 1
        self.mock_metricity_user(joined_at, total_messages, total_blocks)

        # When
        url = reverse('bot:user-metricity-data', args=[0], host='api')
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "joined_at": joined_at,
            "total_messages": total_messages,
            "voice_banned": False,
            "activity_blocks": total_blocks
        })

    def test_no_metricity_user(self):
        # Given
        self.mock_no_metricity_user()

        # When
        url = reverse('bot:user-metricity-data', args=[0], host='api')
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def test_metricity_voice_banned(self):
        cases = [
            {'exception': None, 'voice_banned': True},
            {'exception': ObjectDoesNotExist, 'voice_banned': False},
        ]

        self.mock_metricity_user("foo", 1, 1)

        for case in cases:
            with self.subTest(exception=case['exception'], voice_banned=case['voice_banned']):
                with patch("pydis_site.apps.api.viewsets.bot.user.Infraction.objects.get") as p:
                    p.side_effect = case['exception']

                    url = reverse('bot:user-metricity-data', args=[0], host='api')
                    response = self.client.get(url)

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["voice_banned"], case["voice_banned"])

    def mock_metricity_user(self, joined_at, total_messages, total_blocks):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.return_value = dict(joined_at=joined_at)
        self.metricity.total_messages.return_value = total_messages
        self.metricity.total_message_blocks.return_value = total_blocks

    def mock_no_metricity_user(self):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.side_effect = NotFound()
        self.metricity.total_messages.side_effect = NotFound()
        self.metricity.total_message_blocks.side_effect = NotFound()
