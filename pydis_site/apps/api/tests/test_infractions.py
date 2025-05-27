import datetime
from datetime import UTC, datetime as dt, timedelta
from unittest.mock import patch
from urllib.parse import quote

from django.db import transaction
from django.db.utils import IntegrityError
from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import Infraction, User
from pydis_site.apps.api.serializers import InfractionSerializer


class UnauthenticatedTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_detail_lookup_returns_401(self):
        url = reverse('api:bot:infraction-detail', args=(6,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_list_returns_401(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_create_returns_401(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.post(url, data={'reason': 'Have a nice day.'})

        self.assertEqual(response.status_code, 401)

    def test_partial_update_returns_401(self):
        url = reverse('api:bot:infraction-detail', args=(6,))
        response = self.client.patch(url, data={'reason': 'Have a nice day.'})

        self.assertEqual(response.status_code, 401)


class InfractionTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=6,
            name='james',
            discriminator=1,
        )
        cls.ban_hidden = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='ban',
            reason='He terk my jerb!',
            hidden=True,
            inserted_at=dt(2020, 10, 10, 0, 0, 0, tzinfo=UTC),
            expires_at=dt(5018, 11, 20, 15, 52, tzinfo=UTC),
            active=True,
        )
        cls.ban_inactive = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='ban',
            reason='James is an ass, and we won\'t be working with him again.',
            active=False,
            inserted_at=dt(2020, 10, 10, 0, 1, 0, tzinfo=UTC),
        )
        cls.timeout_permanent = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='timeout',
            reason='He has a filthy mouth and I am his soap.',
            active=True,
            inserted_at=dt(2020, 10, 10, 0, 2, 0, tzinfo=UTC),
            expires_at=None,
        )
        cls.superstar_expires_soon = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='superstar',
            reason='This one doesn\'t matter anymore.',
            active=True,
            inserted_at=dt(2020, 10, 10, 0, 3, 0, tzinfo=UTC),
            expires_at=dt.now(UTC) + datetime.timedelta(hours=5),
        )
        cls.voiceban_expires_later = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='voice_ban',
            reason='Jet engine mic',
            active=True,
            inserted_at=dt(2020, 10, 10, 0, 4, 0, tzinfo=UTC),
            expires_at=dt.now(UTC) + datetime.timedelta(days=5),
        )

    def test_list_all(self):
        """Tests the list-view, which should be ordered by inserted_at (newest first)."""
        url = reverse('api:bot:infraction-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 5)
        self.assertEqual(infractions[0]['id'], self.voiceban_expires_later.id)
        self.assertEqual(infractions[1]['id'], self.superstar_expires_soon.id)
        self.assertEqual(infractions[2]['id'], self.timeout_permanent.id)
        self.assertEqual(infractions[3]['id'], self.ban_inactive.id)
        self.assertEqual(infractions[4]['id'], self.ban_hidden.id)

    def test_filter_search(self):
        url = reverse('api:bot:infraction-list')
        pattern = quote(r'^James(\s\w+){3},')
        response = self.client.get(f'{url}?search={pattern}')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 1)
        self.assertEqual(infractions[0]['id'], self.ban_inactive.id)

    def test_filter_field(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?type=ban&hidden=true')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 1)
        self.assertEqual(infractions[0]['id'], self.ban_hidden.id)

    def test_filter_permanent_false(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?type=timeout&permanent=false')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 0)

    def test_filter_permanent_true(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?type=timeout&permanent=true')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(infractions[0]['id'], self.timeout_permanent.id)

    def test_filter_after(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=5)
        response = self.client.get(url, {'type': 'superstar', 'expires_after': target_time.isoformat()})

        self.assertEqual(response.status_code, 200)
        infractions = response.json()
        self.assertEqual(len(infractions), 0)

    def test_filter_before(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=5)
        response = self.client.get(url, {'type': 'superstar', 'expires_before': target_time.isoformat()})

        self.assertEqual(response.status_code, 200)
        infractions = response.json()
        self.assertEqual(len(infractions), 1)
        self.assertEqual(infractions[0]['id'], self.superstar_expires_soon.id)

    def test_filter_after_invalid(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?expires_after=gibberish')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(next(iter(response.json())), "expires_after")

    def test_filter_before_invalid(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?expires_before=000000000')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(next(iter(response.json())), "expires_before")

    def test_after_before_before(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=4)
        target_time_late = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=6)
        response = self.client.get(
            url,
            {'expires_before': target_time_late.isoformat(),
             'expires_after': target_time.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.superstar_expires_soon.id)

    def test_after_after_before_invalid(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=5)
        target_time_late = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=9)
        response = self.client.get(
            url,
            {'expires_before': target_time.isoformat(),
             'expires_after': target_time_late.isoformat()},
        )

        self.assertEqual(response.status_code, 400)
        errors = list(response.json())
        self.assertIn("expires_before", errors)
        self.assertIn("expires_after", errors)

    def test_permanent_after_invalid(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=5)
        response = self.client.get(
            url,
            {'permanent': 'true', 'expires_after': target_time.isoformat()},
        )

        self.assertEqual(response.status_code, 400)
        errors = list(response.json())
        self.assertEqual("permanent", errors[0])

    def test_permanent_before_invalid(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=5)
        response = self.client.get(
            url,
            {'permanent': 'true', 'expires_before': target_time.isoformat()},
        )

        self.assertEqual(response.status_code, 400)
        errors = list(response.json())
        self.assertEqual("permanent", errors[0])

    def test_nonpermanent_before(self):
        url = reverse('api:bot:infraction-list')
        target_time = datetime.datetime.now(tz=UTC) + datetime.timedelta(hours=6)
        response = self.client.get(
            url,
            {'permanent': 'false', 'expires_before': target_time.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.superstar_expires_soon.id)

    def test_filter_manytypes(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?types=timeout,ban')

        self.assertEqual(response.status_code, 200)
        infractions = response.json()
        self.assertEqual(len(infractions), 3)

    def test_types_type_invalid(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?types=timeout,ban&type=superstar')

        self.assertEqual(response.status_code, 400)
        errors = list(response.json())
        self.assertEqual("types", errors[0])

    def test_sort_expiresby(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?ordering=expires_at&permanent=false')
        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 3)
        self.assertEqual(infractions[0]['id'], self.superstar_expires_soon.id)
        self.assertEqual(infractions[1]['id'], self.voiceban_expires_later.id)
        self.assertEqual(infractions[2]['id'], self.ban_hidden.id)

    def test_returns_empty_for_no_match(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?type=ban&search=poop')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_ignores_bad_filters(self):
        url = reverse('api:bot:infraction-list')
        response = self.client.get(f'{url}?type=ban&hidden=maybe&foo=bar')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve_single_from_id(self):
        url = reverse('api:bot:infraction-detail', args=(self.ban_inactive.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.ban_inactive.id)

    def test_retrieve_returns_404_for_absent_id(self):
        url = reverse('api:bot:infraction-detail', args=(1337,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_partial_update(self):
        url = reverse('api:bot:infraction-detail', args=(self.ban_hidden.id,))
        data = {
            'expires_at': '4143-02-15T21:04:31+00:00',
            'active': False,
            'reason': 'durka derr'
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        infraction = Infraction.objects.get(id=self.ban_hidden.id)

        # These fields were updated.
        self.assertEqual(infraction.expires_at.isoformat(), data['expires_at'])
        self.assertEqual(infraction.active, data['active'])
        self.assertEqual(infraction.reason, data['reason'])

        # These fields are still the same.
        self.assertEqual(infraction.id, self.ban_hidden.id)
        self.assertEqual(infraction.inserted_at, self.ban_hidden.inserted_at)
        self.assertEqual(infraction.user.id, self.ban_hidden.user.id)
        self.assertEqual(infraction.actor.id, self.ban_hidden.actor.id)
        self.assertEqual(infraction.type, self.ban_hidden.type)
        self.assertEqual(infraction.hidden, self.ban_hidden.hidden)

    def test_partial_update_of_inactive_infraction(self):
        url = reverse('api:bot:infraction-detail', args=(self.ban_hidden.id,))
        data = {
            'expires_at': '4143-02-15T21:04:31+00:00',
            'reason': "Do not help out Joe with any electricity-related questions"
        }
        self.assertFalse(self.ban_inactive.active, "Infraction should start out as inactive")
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        infraction = Infraction.objects.get(id=self.ban_inactive.id)
        self.assertFalse(infraction.active, "Infraction changed to active via patch")

    def test_partial_update_returns_400_for_frozen_field(self):
        url = reverse('api:bot:infraction-detail', args=(self.ban_hidden.id,))
        data = {'user': 6}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['This field cannot be updated.']
        })


class CreationTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=5,
            name='james',
            discriminator=1,
        )
        cls.second_user = User.objects.create(
            id=6,
            name='carl',
            discriminator=2,
        )

    def test_accepts_valid_data(self):
        url = reverse('api:bot:infraction-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'reason': 'He terk my jerb!',
            'hidden': True,
            'expires_at': '5018-11-20T15:52:00+00:00',
            'active': True,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        infraction = Infraction.objects.get(id=response.json()['id'])
        self.assertAlmostEqual(
            infraction.inserted_at,
            dt.now(UTC),
            delta=timedelta(seconds=2)
        )
        self.assertEqual(infraction.expires_at.isoformat(), data['expires_at'])
        self.assertEqual(infraction.user.id, data['user'])
        self.assertEqual(infraction.actor.id, data['actor'])
        self.assertEqual(infraction.type, data['type'])
        self.assertEqual(infraction.reason, data['reason'])
        self.assertEqual(infraction.hidden, data['hidden'])
        self.assertEqual(infraction.active, True)

    def test_returns_400_for_missing_user(self):
        url = reverse('api:bot:infraction-list')
        data = {
            'actor': self.user.id,
            'type': 'kick',
            'active': False,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['This field is required.']
        })

    def test_returns_400_for_bad_user(self):
        url = reverse('api:bot:infraction-list')
        data = {
            'user': 1337,
            'actor': self.user.id,
            'type': 'kick',
            'active': True,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['Invalid pk "1337" - object does not exist.']
        })

    def test_returns_400_for_bad_type(self):
        url = reverse('api:bot:infraction-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'hug',
            'active': True,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'type': ['"hug" is not a valid choice.']
        })

    def test_returns_400_for_bad_expired_at_format(self):
        url = reverse('api:bot:infraction-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'expires_at': '20/11/5018 15:52:00',
            'active': True,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'expires_at': [
                'Datetime has wrong format. Use one of these formats instead: '
                'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
            ]
        })

    def test_returns_400_for_expiring_non_expirable_type(self):
        url = reverse('api:bot:infraction-list')

        for infraction_type in ('kick', 'warning'):
            data = {
                'user': self.user.id,
                'actor': self.user.id,
                'type': infraction_type,
                'expires_at': '5018-11-20T15:52:00+00:00',
                'active': False,
            }

            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {
                'expires_at': [f'{data["type"]} infractions cannot expire.']
            })

    def test_returns_400_for_hidden_non_hideable_type(self):
        url = reverse('api:bot:infraction-list')

        for infraction_type in ('superstar', 'warning'):
            data = {
                'user': self.user.id,
                'actor': self.user.id,
                'type': infraction_type,
                'hidden': True,
                'active': False,
            }

            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {
                'hidden': [f'{data["type"]} infractions cannot be hidden.']
            })

    def test_returns_400_for_non_hidden_required_hidden_type(self):
        url = reverse('api:bot:infraction-list')

        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'note',
            'hidden': False,
            'active': False,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'hidden': [f'{data["type"]} infractions must be hidden.']
        })

    def test_returns_400_for_active_infraction_of_type_that_cannot_be_active(self):
        """Test if the API rejects active infractions for types that cannot be active."""
        url = reverse('api:bot:infraction-list')
        restricted_types = (
            ('note', True),
            ('warning', False),
            ('kick', False),
        )

        for infraction_type, hidden in restricted_types:
            # https://stackoverflow.com/a/23326971
            with self.subTest(infraction_type=infraction_type):
                invalid_infraction = {
                    'user': self.user.id,
                    'actor': self.user.id,
                    'type': infraction_type,
                    'reason': 'Take me on!',
                    'hidden': hidden,
                    'active': True,
                    'expires_at': None,
                }
                response = self.client.post(url, data=invalid_infraction)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.json(),
                    {'active': [f'{infraction_type} infractions cannot be active.']}
                )

    def test_returns_400_for_second_active_infraction_of_the_same_type(self):
        """Test if the API rejects a second active infraction of the same type for a given user."""
        url = reverse('api:bot:infraction-list')
        active_infraction_types = ('timeout', 'ban', 'superstar')

        for infraction_type in active_infraction_types:
            with self.subTest(infraction_type=infraction_type), transaction.atomic():
                first_active_infraction = {
                    'user': self.user.id,
                    'actor': self.user.id,
                    'type': infraction_type,
                    'reason': 'Take me on!',
                    'active': True,
                    'expires_at': '2019-10-04T12:52:00+00:00'
                }

                # Post the first active infraction of a type and confirm it's accepted.
                first_response = self.client.post(url, data=first_active_infraction)
                self.assertEqual(first_response.status_code, 201)

                second_active_infraction = {
                    'user': self.user.id,
                    'actor': self.user.id,
                    'type': infraction_type,
                    'reason': 'Take on me!',
                    'active': True,
                    'expires_at': '2019-10-04T12:52:00+00:00'
                }
                second_response = self.client.post(url, data=second_active_infraction)
                self.assertEqual(second_response.status_code, 400)
                self.assertEqual(
                    second_response.json(),
                    {
                        'non_field_errors': [
                            'The fields user, type must make a unique set.'
                        ]
                    }
                )

    def test_returns_201_for_second_active_infraction_of_different_type(self):
        """Test if the API accepts a second active infraction of a different type than the first."""
        url = reverse('api:bot:infraction-list')
        first_active_infraction = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'timeout',
            'reason': 'Be silent!',
            'hidden': True,
            'active': True,
            'expires_at': '2019-10-04T12:52:00+00:00'
        }
        second_active_infraction = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'reason': 'Be gone!',
            'hidden': True,
            'active': True,
            'expires_at': '2019-10-05T12:52:00+00:00'
        }
        # Post the first active infraction of a type and confirm it's accepted.
        first_response = self.client.post(url, data=first_active_infraction)
        self.assertEqual(first_response.status_code, 201)

        # Post the first active infraction of a type and confirm it's accepted.
        second_response = self.client.post(url, data=second_active_infraction)
        self.assertEqual(second_response.status_code, 201)

    def test_unique_constraint_raises_integrity_error_on_second_active_of_same_type(self):
        """Do we raise `IntegrityError` for the second active infraction of a type for a user?"""
        Infraction.objects.create(
            user=self.user,
            actor=self.user,
            type="ban",
            active=True,
            reason="The first active ban"
        )
        with self.assertRaises(IntegrityError):
            Infraction.objects.create(
                user=self.user,
                actor=self.user,
                type="ban",
                active=True,
                reason="The second active ban"
            )

    def test_unique_constraint_accepts_active_infraction_after_inactive_infraction(self):
        """Do we accept an active infraction if the others of the same type are inactive?"""
        try:
            Infraction.objects.create(
                user=self.user,
                actor=self.user,
                type="ban",
                active=False,
                reason="The first inactive ban"
            )
            Infraction.objects.create(
                user=self.user,
                actor=self.user,
                type="ban",
                active=False,
                reason="The second inactive ban"
            )
            Infraction.objects.create(
                user=self.user,
                actor=self.user,
                type="ban",
                active=True,
                reason="The first active ban"
            )
        except IntegrityError:
            self.fail("An unexpected IntegrityError was raised.")

    @patch(f"{__name__}.Infraction")
    def test_if_accepts_active_infraction_test_catches_integrity_error(self, infraction_patch):
        """Does the test properly catch the IntegrityError and raise an AssertionError?"""
        infraction_patch.objects.create.side_effect = IntegrityError
        with self.assertRaises(AssertionError, msg="An unexpected IntegrityError was raised."):
            self.test_unique_constraint_accepts_active_infraction_after_inactive_infraction()

    def test_unique_constraint_accepts_second_active_of_different_type(self):
        """Do we accept a second active infraction of a different type for a given user?"""
        Infraction.objects.create(
            user=self.user,
            actor=self.user,
            type="ban",
            active=True,
            reason="The first active ban"
        )
        Infraction.objects.create(
            user=self.user,
            actor=self.user,
            type="timeout",
            active=True,
            reason="The first active timeout"
        )

    def test_unique_constraint_accepts_active_infractions_for_different_users(self):
        """Do we accept two active infractions of the same type for two different users?"""
        Infraction.objects.create(
            user=self.user,
            actor=self.user,
            type="ban",
            active=True,
            reason="An active ban for the first user"
        )
        Infraction.objects.create(
            user=self.second_user,
            actor=self.second_user,
            type="ban",
            active=False,
            reason="An active ban for the second user"
        )

    def test_integrity_error_if_missing_active_field(self):
        pattern = (
            'null value in column "active" (of relation "api_infraction" )?'
            'violates not-null constraint'
        )
        with self.assertRaisesRegex(IntegrityError, pattern):
            Infraction.objects.create(
                user=self.user,
                actor=self.user,
                type='ban',
                reason='A reason.',
            )

    def test_accepts_two_warnings(self):
        """Two warnings can be created for a user."""
        url = reverse('api:bot:infraction-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'warning',
            'reason': "Thought upgrading DRF is a smart idea",
            'active': False,
        }
        first_response = self.client.post(url, data=data)
        self.assertEqual(first_response.status_code, 201)
        data['reason'] = "Do not claim King Arthur eats children"
        second_response = self.client.post(url, data=data)
        self.assertEqual(second_response.status_code, 201)

    def test_respects_active_false_of_warnings(self):
        """Infractions can be created as inactive."""
        url = reverse('api:bot:infraction-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'warning',
            'reason': "Associate of REDACTED",
            'active': False,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        infraction = Infraction.objects.get(id=response.json()['id'])
        self.assertFalse(infraction.active)


class InfractionDeletionTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=9876,
            name='Unknown user',
            discriminator=9876,
        )

        cls.warning = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='warning',
            active=False
        )

    def test_delete_unknown_infraction_returns_404(self):
        url = reverse('api:bot:infraction-detail', args=('something',))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_delete_known_infraction_returns_204(self):
        url = reverse('api:bot:infraction-detail', args=(self.warning.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertRaises(Infraction.DoesNotExist, Infraction.objects.get, id=self.warning.id)


class ExpandedTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=5,
            name='james',
            discriminator=1,
        )
        cls.kick = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='kick',
            active=False
        )
        cls.warning = Infraction.objects.create(
            user_id=cls.user.id,
            actor_id=cls.user.id,
            type='warning',
            active=False,
        )

    def check_expanded_fields(self, infraction):
        for key in ('user', 'actor'):
            obj = infraction[key]
            for field in ('id', 'name', 'discriminator', 'roles', 'in_guild'):
                self.assertTrue(field in obj, msg=f'field "{field}" missing from {key}')
            if key == 'user':
                self.assertIn('alts', obj)

    def test_list_expanded(self):
        url = reverse('api:bot:infraction-list-expanded')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        for infraction in response_data:
            self.check_expanded_fields(infraction)

    def test_create_expanded(self):
        url = reverse('api:bot:infraction-list-expanded')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'warning',
            'active': False
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(Infraction.objects.all()), 3)
        self.check_expanded_fields(response.json())

    def test_retrieve_expanded(self):
        url = reverse('api:bot:infraction-detail-expanded', args=(self.warning.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        infraction = response.json()
        self.assertEqual(infraction['id'], self.warning.id)
        self.check_expanded_fields(infraction)

    def test_partial_update_expanded(self):
        url = reverse('api:bot:infraction-detail-expanded', args=(self.kick.id,))
        data = {'active': False}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        infraction = Infraction.objects.get(id=self.kick.id)
        self.assertEqual(infraction.active, data['active'])
        self.check_expanded_fields(response.json())


class SerializerTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=5,
            name='james',
            discriminator=1,
        )

    def create_infraction(self, _type: str, active: bool):
        return Infraction.objects.create(
            user_id=self.user.id,
            actor_id=self.user.id,
            type=_type,
            reason='A reason.',
            expires_at=dt(5018, 11, 20, 15, 52, tzinfo=UTC),
            active=active
        )

    def test_is_valid_if_active_infraction_with_same_fields_exists(self):
        self.create_infraction('ban', active=True)
        instance = self.create_infraction('ban', active=False)

        data = {'reason': 'hello', 'active': True}
        serializer = InfractionSerializer(instance, data=data, partial=True)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    def test_is_valid_for_new_active_infraction(self):
        self.create_infraction('ban', active=False)

        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'reason': 'A reason.',
            'active': True
        }
        serializer = InfractionSerializer(data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    def test_validation_error_if_missing_active_field(self):
        data = {
            'user': self.user.id,
            'actor': self.user.id,
            'type': 'ban',
            'reason': 'A reason.',
        }
        serializer = InfractionSerializer(data=data)

        if not serializer.is_valid():
            self.assertIn('active', serializer.errors)

            code = serializer.errors['active'][0].code
            msg = f'Expected failure on required active field but got {serializer.errors}'
            self.assertEqual(code, 'required', msg=msg)
        else:  # pragma: no cover
            self.fail('Validation unexpectedly succeeded.')
