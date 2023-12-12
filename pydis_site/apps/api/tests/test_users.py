import random
from unittest.mock import Mock, patch

from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import Infraction, Role, User, UserAltRelationship
from pydis_site.apps.api.models.bot.metricity import NotFoundError
from pydis_site.apps.api.viewsets.bot.user import UserListPagination


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
            'name': "test",
            'display_name': "Test Display",
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
        self.assertEqual(user.display_name, data['display_name'])
        self.assertEqual(user.discriminator, data['discriminator'])
        self.assertEqual(user.in_guild, data['in_guild'])

    def test_supports_multi_creation(self):
        url = reverse('api:bot:user-list')
        data = [
            {
                'id': 5,
                'name': "testman",
                'display_name': "Test Display 1",
                'discriminator': 42,
                'roles': [
                    self.role.id
                ],
                'in_guild': True
            },
            {
                'id': 8,
                'name': "anothertestman",
                'display_name': "Test Display 2",
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
                "name": "user1patched",
                "display_name": "User 1 Patched",
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
            ), patch("pydis_site.apps.api.viewsets.bot.user.Infraction.objects.filter") as p:
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
        self.metricity.total_messages_in_past_n_days.return_value = [(0, 10)]

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
        self.assertEqual(response.json(), {"0": 10, "1": 0})

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


class UserAltUpdateTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            id=12095219,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.user_2 = User.objects.create(
            id=18259125,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )

    def test_adding_existing_alt(self) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_2.id,
            'actor': self.user_1.id,
            'context': "Joe's trolling account"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 204)

        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()

        self.assertQuerySetEqual(self.user_1.alts.all(), [self.user_2])
        self.assertQuerySetEqual(self.user_2.alts.all(), [self.user_1])

        detail_url = reverse('api:bot:user-detail', args=(self.user_1.id,))
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)

        parsed_detail = detail_response.json()
        [parsed_alt] = parsed_detail.pop('alts')
        parsed_alt.pop('created_at')
        parsed_alt.pop('updated_at')

        self.assertEqual(
            parsed_detail,
            {
                'id': self.user_1.id,
                'name': self.user_1.name,
                'display_name': self.user_1.display_name,
                'discriminator': self.user_1.discriminator,
                'roles': self.user_1.roles,
                'in_guild': self.user_1.in_guild,
            }
        )
        self.assertEqual(
            parsed_alt,
            {
                'source': self.user_1.id,
                'target': data['target'],
                'alts': [self.user_1.id],
                'actor': data['actor'],
                'context': data['context'],
            }
        )

    def test_adding_existing_alt_twice_via_source(self) -> None:
        self.verify_adding_existing_alt(add_on_source=True)

    def test_adding_existing_alt_twice_via_target(self) -> None:
        self.verify_adding_existing_alt(add_on_source=False)

    def verify_adding_existing_alt(self, add_on_source: bool) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_2.id,
            'actor': self.user_1.id,
            'context': "Lemon's trolling account"
        }
        initial_response = self.client.post(url, data)
        self.assertEqual(initial_response.status_code, 204)

        if add_on_source:
            repeated_url = url
            repeated_data = data
        else:
            repeated_url = reverse('api:bot:user-alts', args=(self.user_2.id,))
            repeated_data = {
                'target': self.user_1.id,
                'actor': self.user_1.id,
                'context': data['context']
            }

        response = self.client.post(repeated_url, repeated_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'source': ["This relationship has already been established"]
        })

    def test_removing_existing_alt_source_from_target(self) -> None:
        self.verify_deletion(delete_on_source=False)

    def test_removing_existing_alt_target_from_source(self) -> None:
        self.verify_deletion(delete_on_source=True)

    def verify_deletion(self, delete_on_source: bool) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_2.id,
            'actor': self.user_1.id,
            'context': "Lemon's trolling account"
        }
        initial_response = self.client.post(url, data)
        self.assertEqual(initial_response.status_code, 204)

        self.assertTrue(self.user_1.alts.all().exists())
        self.assertTrue(self.user_2.alts.all().exists())

        if delete_on_source:
            data = self.user_2.id
            alts_url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        else:
            data = self.user_1.id
            alts_url = reverse('api:bot:user-alts', args=(self.user_2.id,))

        response = self.client.delete(alts_url, data)

        self.assertEqual(response.status_code, 204)

        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()

        self.assertFalse(self.user_1.alts.all().exists())
        self.assertFalse(self.user_2.alts.all().exists())

    def test_removing_unknown_alt(self) -> None:
        data = self.user_1.id + self.user_2.id
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Specified account is not a known alternate account of this user"]
        })

    def test_add_alt_returns_error_for_missing_keys_in_request_body(self) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {'hello': 'joe'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_remove_alt_returns_error_for_non_int_request_body(self) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {'hello': 'joe'}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, 400)

    def test_adding_alt_to_user_that_does_not_exist(self) -> None:
        """Patching a user's alts for a user that doesn't exist should return a 404."""
        url = reverse('api:bot:user-alts', args=(self.user_1.id + self.user_2.id,))
        data = {
            'target': self.user_2.id,
            'actor': self.user_1.id,
            'context': "Chris's trolling account"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_adding_alt_that_does_not_exist_to_user(self) -> None:
        """Patching a user's alts with an alt that is unknown should return a 400."""
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_1.id + self.user_2.id,
            'actor': self.user_1.id,
            'context': "Hello, Joe"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'target': [f'Invalid pk "{data["target"]}" - object does not exist.']
        })

    def test_cannot_add_self_as_alt_account(self) -> None:
        """The existing account may not be an alt of itself."""
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_1.id,
            'actor': self.user_1.id,
            'context': "Schizophrenia"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'source': ["The user may not be an alternate account of itself"]
        })

    def test_cannot_update_alts_on_regular_user_patch_route(self) -> None:
        """The regular user update route does not allow editing the alts."""
        url = reverse('api:bot:user-detail', args=(self.user_1.id,))
        data = {'alts': [self.user_2.id]}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)  # XXX: This seems to be a DRF bug

        self.user_1.refresh_from_db()
        self.assertQuerySetEqual(self.user_1.alts.all(), ())
        self.user_2.refresh_from_db()
        self.assertQuerySetEqual(self.user_2.alts.all(), ())

    def test_cannot_update_alts_on_bulk_user_patch_route(self) -> None:
        """The bulk user update route does not allow editing the alts."""
        url = reverse('api:bot:user-bulk-patch')
        data = [{'id': self.user_1.id, 'alts': [self.user_2.id]}]
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'non_field_errors': ['Insufficient data provided.']})

        self.user_1.refresh_from_db()
        self.assertQuerySetEqual(self.user_1.alts.all(), ())
        self.user_2.refresh_from_db()
        self.assertQuerySetEqual(self.user_2.alts.all(), ())

    def test_user_bulk_patch_does_not_discard_alts(self) -> None:
        """The bulk user update route should not modify the alts."""
        alts_url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        data = {
            'target': self.user_2.id,
            'actor': self.user_2.id,
            'context': "This is my testing account"
        }
        alts_response = self.client.post(alts_url, data)
        self.assertEqual(alts_response.status_code, 204)

        url = reverse('api:bot:user-bulk-patch')
        self.user_1.alts.set((self.user_2,))
        data = [{'id': self.user_1.id, 'name': "Joe Armstrong"}]
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

        self.user_1.refresh_from_db()
        self.assertQuerySetEqual(self.user_1.alts.all(), (self.user_2,))
        self.user_2.refresh_from_db()
        self.assertQuerySetEqual(self.user_2.alts.all(), (self.user_1,))


class UserAltUpdateWithExistingAltsTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            id=12095219,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.user_2 = User.objects.create(
            id=18259125,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.relationship_1 = UserAltRelationship.objects.create(
            source=cls.user_1,
            target=cls.user_2,
            context="Test user's trolling account",
            actor=cls.user_1
        )
        cls.relationship_2 = UserAltRelationship.objects.create(
            source=cls.user_2,
            target=cls.user_1,
            context="Test user's trolling account",
            actor=cls.user_1
        )

    def test_returns_404_for_unknown_user(self) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id + self.user_2.id,))
        response = self.client.patch(url, {'target': self.user_2.id, 'context': "Dinoman"})
        self.assertEqual(response.status_code, 404)

    def test_returns_400_for_unknown_alt_from_source(self) -> None:
        self.verify_returns_400_for_unknown_alt(from_source=True)

    def test_returns_400_for_unknown_alt_from_target(self) -> None:
        self.verify_returns_400_for_unknown_alt(from_source=False)

    def verify_returns_400_for_unknown_alt(self, from_source: bool) -> None:
        if from_source:
            source = self.user_1.id
        else:
            source = self.user_2.id

        target = self.user_1.id + self.user_2.id

        url = reverse('api:bot:user-alts', args=(source,))
        data = {'target': target, 'context': "Still a trolling account"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'target': ["User is not an associated alt account"]
        })

    def test_returns_400_for_missing_fields(self) -> None:
        url = reverse('api:bot:user-alts', args=(self.user_1.id,))
        payloads = [{'target': self.user_2.id}, {'context': "Confirmed"}]
        for payload in payloads:
            key = next(iter(payload))
            (missing_key,) = tuple({'target', 'context'} - {key})
            with self.subTest(specified_key=next(iter(payload))):
                response = self.client.patch(url, payload)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json(), {
                    missing_key: ["This field is required."]
                })

    def test_accepts_valid_update_from_source(self) -> None:
        self.verify_accepts_valid_update(from_source=True)

    def test_accepts_valid_update_from_target(self) -> None:
        self.verify_accepts_valid_update(from_source=False)

    def verify_accepts_valid_update(self, from_source: bool) -> None:
        if from_source:
            source = self.user_1.id
            target = self.user_2.id
        else:
            source = self.user_2.id
            target = self.user_1.id

        url = reverse('api:bot:user-alts', args=(source,))
        data = {'target': target, 'context': "Still a trolling account"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 204)

        self.relationship_1.refresh_from_db()
        self.relationship_2.refresh_from_db()
        self.assertEqual(self.relationship_1.context, data['context'])
        self.assertEqual(self.relationship_2.context, data['context'])

    def test_retrieving_alts_via_source(self) -> None:
        self.verify_retrieving_alts(from_source=True)

    def test_retrieving_alts_via_target(self) -> None:
        self.verify_retrieving_alts(from_source=False)

    def verify_retrieving_alts(self, from_source: bool) -> None:
        if from_source:
            source = self.user_1.id
            target = self.user_2.id
        else:
            source = self.user_2.id
            target = self.user_1.id

        url = reverse('api:bot:user-detail', args=(source,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        [alt] = body['alts']
        alt.pop('created_at')
        alt.pop('updated_at')
        self.assertEqual(alt,
            {
                'actor': self.relationship_1.actor.id,
                'source': source,
                'alts': [source],
                'target': target,
                'context': self.relationship_1.context
            }
        )


class UserAltUpdateWithExistingTransitiveAltsTests(AuthenticatedAPITestCase):
    """
    Test user alt methods via transitive alternate account relationships.

    Specifically, user 2 is an alt account of user 1, and user 3 is an alt
    account of user 2. However, user 3 should not be an alt account of
    user 1 in this case.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            id=12095219,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.user_2 = User.objects.create(
            id=18259125,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.user_3 = User.objects.create(
            id=18294612591,
            name=f"Test user {random.randint(100, 1000)}",
            discriminator=random.randint(1, 9999),
            in_guild=True,
        )
        cls.relationship_1 = UserAltRelationship.objects.create(
            source=cls.user_1,
            target=cls.user_2,
            context="Test user's trolling account (rel 1, U1 -> U2)",
            actor=cls.user_1
        )
        cls.relationship_2 = UserAltRelationship.objects.create(
            source=cls.user_2,
            target=cls.user_1,
            context="Test user's trolling account (rel 2, U2 -> U1)",
            actor=cls.user_1
        )
        cls.relationship_3 = UserAltRelationship.objects.create(
            source=cls.user_2,
            target=cls.user_3,
            context="Test user's trolling account (rel 3, U2 -> U3)",
            actor=cls.user_2
        )
        cls.relationship_4 = UserAltRelationship.objects.create(
            source=cls.user_3,
            target=cls.user_2,
            context="Test user's trolling account (rel 4, U3 -> U2)",
            actor=cls.user_2
        )

    def test_retrieving_alts_via_source(self) -> None:
        subtests = [
            # Source user, Expected sub-alts of each alt
            # U1, ({U2 -> {U1, U3}},)
            (self.user_1.id, ({self.user_1.id, self.user_3.id},)),
            # U2, ({U1 -> U2}, {U3 -> U2},)
            (self.user_2.id, ({self.user_2.id}, {self.user_2.id})),
            # U3, ({U2 -> {U1, U3}},)
            (self.user_3.id, ({self.user_1.id, self.user_3.id},)),
        ]

        for (source, expected_subalts) in subtests:
            with self.subTest(source=source):
                url = reverse('api:bot:user-detail', args=(source,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                body = response.json()
                for alt, subalts in zip(body['alts'], expected_subalts, strict=True):
                    alt.pop('created_at')
                    alt.pop('updated_at')

                    self.assertEqual(len(set(alt['alts'])), len(subalts))
                    self.assertEqual(set(alt['alts']), subalts)
                    self.assertEqual(alt['source'], source)
