from datetime import UTC, datetime as dt, timedelta

from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import Nomination, NominationEntry, User


class CreationTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=1234,
            name='joe dart',
            discriminator=1111,
        )
        cls.user2 = User.objects.create(
            id=9876,
            name='Who?',
            discriminator=1234
        )

    def test_accepts_valid_data(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'actor': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'user': self.user.id,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        nomination = Nomination.objects.get(id=response.json()['id'])
        nomination_entry = NominationEntry.objects.get(
            nomination_id=nomination.id,
            actor_id=self.user.id
        )
        self.assertAlmostEqual(
            nomination.inserted_at,
            dt.now(UTC),
            delta=timedelta(seconds=2)
        )
        self.assertEqual(nomination.user.id, data['user'])
        self.assertEqual(nomination_entry.reason, data['reason'])
        self.assertEqual(nomination.active, True)

    def test_returns_200_on_second_active_nomination_by_different_user(self):
        url = reverse('api:bot:nomination-list')
        first_data = {
            'actor': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'user': self.user.id,
        }
        second_data = {
            'actor': self.user2.id,
            'reason': 'Great user',
            'user': self.user.id
        }

        response1 = self.client.post(url, data=first_data)
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(url, data=second_data)
        self.assertEqual(response2.status_code, 201)

    def test_returns_400_on_second_active_nomination_by_existing_nominator(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'actor': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'user': self.user.id,
        }

        response1 = self.client.post(url, data=data)
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(url, data=data)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json(), {
            'actor': ['This actor has already endorsed this nomination.']
        })

    def test_returns_400_for_missing_user(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'actor': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['This field is required.']
        })

    def test_returns_400_for_missing_actor(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'actor': ['This field is required.']
        })

    def test_returns_201_for_missing_reason(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'actor': self.user.id,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_returns_400_for_bad_user(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': 1024,
            'reason': 'Joe Dart on Fender Bass',
            'actor': self.user.id,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['Invalid pk "1024" - object does not exist.']
        })

    def test_returns_400_for_bad_actor(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'actor': 1024,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'actor': ['Invalid pk "1024" - object does not exist.']
        })

    def test_returns_400_for_end_reason_at_creation(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'actor': self.user.id,
            'end_reason': "Joe Dart on the Joe Dart Bass"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'end_reason': ['This field cannot be set at creation.']
        })

    def test_returns_400_for_ended_at_at_creation(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'actor': self.user.id,
            'ended_at': "Joe Dart on the Joe Dart Bass"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ended_at': ['This field cannot be set at creation.']
        })

    def test_returns_400_for_inserted_at_at_creation(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'actor': self.user.id,
            'inserted_at': "Joe Dart on the Joe Dart Bass"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'inserted_at': ['This field cannot be set at creation.']
        })

    def test_returns_400_for_active_at_creation(self):
        url = reverse('api:bot:nomination-list')
        data = {
            'user': self.user.id,
            'reason': 'Joe Dart on Fender Bass',
            'actor': self.user.id,
            'active': False
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'active': ['This field cannot be set at creation.']
        })


class NominationTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            id=1234,
            name='joe dart',
            discriminator=1111,
        )

        cls.active_nomination = Nomination.objects.create(
            user=cls.user
        )
        cls.active_nomination_entry = NominationEntry.objects.create(
            nomination=cls.active_nomination,
            actor=cls.user,
            reason="He's pretty funky"
        )
        cls.inactive_nomination = Nomination.objects.create(
            user=cls.user,
            active=False,
            end_reason="His neck couldn't hold the funk",
            ended_at="5018-11-20T15:52:00+00:00"
        )
        cls.inactive_nomination_entry = NominationEntry.objects.create(
            nomination=cls.inactive_nomination,
            actor=cls.user,
            reason="He's pretty funky"
        )

    def test_returns_200_update_reason_on_active_with_actor(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {
            'reason': "He's one funky duck",
            'actor': self.user.id
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        nomination_entry = NominationEntry.objects.get(
            nomination_id=response.json()['id'],
            actor_id=self.user.id
        )
        self.assertEqual(nomination_entry.reason, data['reason'])

    def test_returns_400_on_frozen_field_update(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {
            'user': 1234
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['This field cannot be updated.']
        })

    def test_returns_400_update_end_reason_on_active(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {
            'end_reason': 'He started playing jazz'
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'end_reason': ["An active nomination can't have an end reason."]
        })

    def test_returns_200_update_reason_on_inactive(self):
        url = reverse('api:bot:nomination-detail', args=(self.inactive_nomination.id,))
        data = {
            'reason': "He's one funky duck",
            'actor': self.user.id
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        nomination_entry = NominationEntry.objects.get(
            nomination_id=response.json()['id'],
            actor_id=self.user.id
        )
        self.assertEqual(nomination_entry.reason, data['reason'])

    def test_returns_200_update_end_reason_on_inactive(self):
        url = reverse('api:bot:nomination-detail', args=(self.inactive_nomination.id,))
        data = {
            'end_reason': 'He started playing jazz'
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        nomination = Nomination.objects.get(id=response.json()['id'])
        self.assertEqual(nomination.end_reason, data['end_reason'])

    def test_returns_200_on_valid_end_nomination(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(self.active_nomination.id,),
        )
        data = {
            'active': False,
            'end_reason': 'He started playing jazz'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        nomination = Nomination.objects.get(id=response.json()['id'])

        self.assertAlmostEqual(
            nomination.ended_at,
            dt.now(UTC),
            delta=timedelta(seconds=2)
        )
        self.assertFalse(nomination.active)
        self.assertEqual(nomination.end_reason, data['end_reason'])

    def test_returns_400_on_invalid_field_end_nomination(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(self.active_nomination.id,),
        )
        data = {
            'active': False,
            'reason': 'Why does a whale have feet?',
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'reason': ['This field cannot be set when ending a nomination.']
        })

    def test_returns_400_on_missing_end_reason_end_nomination(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(self.active_nomination.id,),
        )
        data = {
            'active': False,
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'end_reason': ['This field is required when ending a nomination.']
        })

    def test_returns_400_on_invalid_use_of_active(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(self.inactive_nomination.id,),
        )
        data = {
            'active': False,
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'active': ['This field can only be used to end a nomination']
        })

    def test_returns_404_on_get_unknown_nomination(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(9999,),
        )

        response = self.client.get(url, data={})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "detail": "No Nomination matches the given query."
        })

    def test_returns_404_on_patch_unknown_nomination(self):
        url = reverse(
            'api:bot:nomination-detail',
            args=(9999,),
        )

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "detail": "No Nomination matches the given query."
        })

    def test_returns_405_on_list_put(self):
        url = reverse('api:bot:nomination-list')

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"PUT\" not allowed."
        })

    def test_returns_405_on_list_patch(self):
        url = reverse('api:bot:nomination-list')

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"PATCH\" not allowed."
        })

    def test_returns_405_on_list_delete(self):
        url = reverse('api:bot:nomination-list')

        response = self.client.delete(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"DELETE\" not allowed."
        })

    def test_returns_405_on_detail_post(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))

        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"POST\" not allowed."
        })

    def test_returns_405_on_detail_delete(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))

        response = self.client.delete(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"DELETE\" not allowed."
        })

    def test_returns_405_on_detail_put(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {
            "detail": "Method \"PUT\" not allowed."
        })

    def test_filter_returns_0_objects_unknown_user__id(self):
        url = reverse('api:bot:nomination-list')

        response = self.client.get(
            url,
            data={
                "user__id": 99998888
            }
        )

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 0)

    def test_filter_returns_2_objects_for_testdata(self):
        url = reverse('api:bot:nomination-list')

        response = self.client.get(
            url,
            data={
                "user__id": self.user.id
            }
        )

        self.assertEqual(response.status_code, 200)
        infractions = response.json()

        self.assertEqual(len(infractions), 2)

    def test_patch_nomination_set_reviewed_of_active_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'reviewed': True}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_nomination_set_reviewed_of_inactive_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.inactive_nomination.id,))
        data = {'reviewed': True}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'reviewed': ['This field cannot be set if the nomination is inactive.']
        })

    def test_patch_nomination_set_reviewed_and_end(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'reviewed': True, 'active': False, 'end_reason': "What?"}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'reviewed': ['This field cannot be set while you are ending a nomination.']
        })

    def test_modifying_reason_without_actor(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'reason': 'That is my reason!'}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'actor': ['This field is required when editing the reason.']
        })

    def test_modifying_reason_with_unknown_actor(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'reason': 'That is my reason!', 'actor': 90909090909090}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'actor': ["The actor doesn't exist or has not nominated the user."]
        })

    def test_patch_nomination_set_thread_id_of_active_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'thread_id': 9876543210}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_nomination_set_thread_id_and_reviewed_of_active_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'thread_id': 9876543210, "reviewed": True}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_modifying_thread_id_when_ending_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.active_nomination.id,))
        data = {'thread_id': 9876543210, 'active': False, 'end_reason': "What?"}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'thread_id': ['This field cannot be set when ending a nomination.']
        })

    def test_patch_thread_id_for_inactive_nomination(self):
        url = reverse('api:bot:nomination-detail', args=(self.inactive_nomination.id,))
        data = {'thread_id': 9876543210}

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'thread_id': ['This field cannot be set if the nomination is inactive.']
        })
