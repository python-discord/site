import random
from unittest.mock import Mock, patch

from django.urls import reverse

from .base import AuthenticatedAPITestCase
from ..models import Infraction, Role, User
from ..models.bot.metricity import NotFoundError
from ..viewsets.bot.user import UserListPagination


class UnauthedUserAPITests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('api:bot:user-detail', args=('whatever',))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('api:bot:user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('api:bot:user-list')
        response = self.client.post(url, data={'hi': 'there'})

        self.assertEqual(response.status_code, 401)

    def test_delete_returns_401(self):
        url = reverse('api:bot:user-detail', args=('whatever',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)


class CreationTests(AuthenticatedAPITestCase):
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
        url = reverse('api:bot:user-list')
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
        url = reverse('api:bot:user-list')
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
        url = reverse('api:bot:user-list')
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
        url = reverse('api:bot:user-list')
        data = {
            'id': True,
            'discriminator': "totally!"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_user_recreation(self):
        """Return 201 if User is already present in database as it skips User creation."""
        url = reverse('api:bot:user-list')
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
        url = reverse('api:bot:user-list')
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
        url = reverse('api:bot:user-list')
        data = {
            'id': 11,
            'name': 'You saw nothing part 3.',
            'discriminator': 1122,
            'in_guild': True
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)


class MultiPatchTests(AuthenticatedAPITestCase):
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
        url = reverse("api:bot:user-bulk-patch")
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
        url = reverse("api:bot:user-bulk-patch")
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
        url = reverse("api:bot:user-bulk-patch")
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
        url = reverse("api:bot:user-bulk-patch")
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
        url = reverse("api:bot:user-bulk-patch")
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
        url = reverse("api:bot:user-bulk-patch")
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


class UserModelTests(AuthenticatedAPITestCase):
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


class UserPaginatorTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        users = []
        for i in range(1, UserListPagination.page_size + 1):
            users.append(User(
                id=i,
                name=f"user{i}",
                discriminator=1111,
                in_guild=True
            ))
        cls.users = User.objects.bulk_create(users)

    def test_returns_single_page_response(self):
        url = reverse("api:bot:user-list")
        response = self.client.get(url).json()
        self.assertIsNone(response["next_page_no"])
        self.assertIsNone(response["previous_page_no"])

    def test_returns_next_page_number(self):
        user_id = UserListPagination.page_size + 1
        User.objects.create(
            id=user_id,
            name=f"user{user_id}",
            discriminator=1111,
            in_guild=True
        )
        url = reverse("api:bot:user-list")
        response = self.client.get(url).json()
        self.assertEqual(2, response["next_page_no"])

    def test_returns_previous_page_number(self):
        user_id = UserListPagination.page_size + 1
        User.objects.create(
            id=user_id,
            name=f"user{user_id}",
            discriminator=1111,
            in_guild=True
        )
        url = reverse("api:bot:user-list")
        response = self.client.get(url, {"page": 2}).json()
        self.assertEqual(1, response["previous_page_no"])


class UserMetricityTests(AuthenticatedAPITestCase):
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
        self.mock_metricity_user(joined_at, total_messages, total_blocks, [])

        # When
        url = reverse('api:bot:user-metricity-data', args=[0])
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json(), {
            "joined_at": joined_at,
            "total_messages": total_messages,
            "voice_gate_blocked": False,
            "activity_blocks": total_blocks
        })

    def test_no_metricity_user(self):
        # Given
        self.mock_no_metricity_user()

        # When
        url = reverse('api:bot:user-metricity-data', args=[0])
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def test_no_metricity_user_for_review(self):
        # Given
        self.mock_no_metricity_user()

        # When
        url = reverse('api:bot:user-metricity-review-data', args=[0])
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def test_metricity_voice_banned(self):
        queryset_with_values = Mock(spec=Infraction.objects)
        queryset_with_values.filter.return_value = queryset_with_values
        queryset_with_values.exists.return_value = True

        queryset_without_values = Mock(spec=Infraction.objects)
        queryset_without_values.filter.return_value = queryset_without_values
        queryset_without_values.exists.return_value = False
        cases = [
            {'voice_infractions': queryset_with_values, 'voice_gate_blocked': True},
            {'voice_infractions': queryset_without_values, 'voice_gate_blocked': False},
        ]

        self.mock_metricity_user("foo", 1, 1, [["bar", 1]])

        for case in cases:
            with self.subTest(
                voice_infractions=case['voice_infractions'],
                voice_gate_blocked=case['voice_gate_blocked']
            ):
                with patch("pydis_site.apps.api.viewsets.bot.user.Infraction.objects.filter") as p:
                    p.return_value = case['voice_infractions']

                    url = reverse('api:bot:user-metricity-data', args=[0])
                    response = self.client.get(url)

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.json()["voice_gate_blocked"],
                        case["voice_gate_blocked"]
                    )

    def test_metricity_review_data(self):
        # Given
        joined_at = "foo"
        total_messages = 10
        total_blocks = 1
        channel_activity = [["bar", 4], ["buzz", 6]]
        self.mock_metricity_user(joined_at, total_messages, total_blocks, channel_activity)

        # When
        url = reverse('api:bot:user-metricity-review-data', args=[0])
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "joined_at": joined_at,
            "top_channel_activity": channel_activity,
            "total_messages": total_messages
        })

    def test_metricity_activity_data(self):
        # Given
        self.mock_no_metricity_user()  # Other functions shouldn't be used.
        self.metricity.total_messages_in_past_n_days.return_value = [[0, 10]]

        # When
        url = reverse("api:bot:user-metricity-activity-data")
        response = self.client.post(
            url,
            data=[0, 1],
            QUERY_STRING="days=10",
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.metricity.total_messages_in_past_n_days.assert_called_once_with(["0", "1"], 10)
        self.assertEqual(response.json(), [{"id": 0, "message_count": 10}])

    def test_metricity_activity_data_invalid_days(self):
        # Given
        self.mock_no_metricity_user()  # Other functions shouldn't be used.

        # When
        url = reverse("api:bot:user-metricity-activity-data")
        response = self.client.post(
            url,
            data=[0, 1],
            QUERY_STRING="days=fifty",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.metricity.total_messages_in_past_n_days.assert_not_called()
        self.assertEqual(response.json(), {"days": ["This query parameter must be an integer."]})

    def test_metricity_activity_data_no_days(self):
        # Given
        self.mock_no_metricity_user()  # Other functions shouldn't be used.

        # When
        url = reverse('api:bot:user-metricity-activity-data')
        response = self.client.post(
            url,
            data=[0, 1],
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.metricity.total_messages_in_past_n_days.assert_not_called()
        self.assertEqual(response.json(), {'days': ["This query parameter is required."]})

    def test_metricity_activity_data_no_users(self):
        # Given
        self.mock_no_metricity_user()  # Other functions shouldn't be used.

        # When
        url = reverse('api:bot:user-metricity-activity-data')
        response = self.client.post(
            url,
            QUERY_STRING="days=10",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.metricity.total_messages_in_past_n_days.assert_not_called()
        self.assertEqual(response.json(), ['Expected a list of items but got type "dict".'])

    def test_metricity_activity_data_invalid_users(self):
        # Given
        self.mock_no_metricity_user()  # Other functions shouldn't be used.

        # When
        url = reverse('api:bot:user-metricity-activity-data')
        response = self.client.post(
            url,
            data=[123, 'username'],
            QUERY_STRING="days=10",
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.metricity.total_messages_in_past_n_days.assert_not_called()
        self.assertEqual(response.json(), {'1': ['A valid integer is required.']})

    def mock_metricity_user(self, joined_at, total_messages, total_blocks, top_channel_activity):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.return_value = dict(joined_at=joined_at)
        self.metricity.total_messages.return_value = total_messages
        self.metricity.total_message_blocks.return_value = total_blocks
        self.metricity.top_channel_activity.return_value = top_channel_activity

    def mock_no_metricity_user(self):
        patcher = patch("pydis_site.apps.api.viewsets.bot.user.Metricity")
        self.metricity = patcher.start()
        self.addCleanup(patcher.stop)
        self.metricity = self.metricity.return_value.__enter__.return_value
        self.metricity.user.side_effect = NotFoundError()
        self.metricity.total_messages.side_effect = NotFoundError()
        self.metricity.total_message_blocks.side_effect = NotFoundError()
        self.metricity.top_channel_activity.side_effect = NotFoundError()


class UserViewSetTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.searched_user = User.objects.create(
            id=12095219,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.other_user = User.objects.create(
            id=18259125,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )

    def test_search_lookup_of_wanted_user(self) -> None:
        """Searching a user by name and discriminator should return that user."""
        url = reverse('api:bot:user-list')
        params = {
            'username': self.searched_user.name,
            'discriminator': self.searched_user.discriminator,
        }
        response = self.client.get(url, params)
        result = response.json()
        self.assertEqual(result['count'], 1)
        [user] = result['results']
        self.assertEqual(user['id'], self.searched_user.id)

    def test_search_lookup_of_unknown_user(self) -> None:
        """Searching an unknown user should return no results."""
        url = reverse('api:bot:user-list')
        params = {
            'username': "f-string enjoyer",
            'discriminator': 1245,
        }
        response = self.client.get(url, params)
        result = response.json()
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['results'], [])
