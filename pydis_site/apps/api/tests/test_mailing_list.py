from django.urls import reverse

from .base import AuthenticatedAPITestCase
from pydis_site.apps.api.models import MailingList, MailingListSeenItem


class NoMailingListTests(AuthenticatedAPITestCase):
    def test_create_mailing_list(self):
        url = reverse('api:bot:mailinglist-list')
        data = {'name': 'lemon-dev'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

class EmptyMailingListTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list = MailingList.objects.create(name='erlang-dev')

    def test_create_duplicate_mailing_list(self):
        url = reverse('api:bot:mailinglist-list')
        data = {'name': self.list.name}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_mailing_lists(self):
        url = reverse('api:bot:mailinglist-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': self.list.id, 'name': self.list.name, 'seen_items': []}
        ])

    def test_get_single_mailing_list(self):
        url = reverse('api:bot:mailinglist-detail', args=(self.list.name,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': self.list.id, 'name': self.list.name, 'seen_items': []
        })

    def test_add_seen_item_to_mailing_list(self):
        data = 'PEP-123'
        url = reverse('api:bot:mailinglist-seen-items', args=(self.list.name,))
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 204)
        self.list.refresh_from_db()
        self.assertEqual(self.list.seen_items.first().hash, data)

    def test_invalid_request_body(self):
        data = [
            "Dinoman, such tiny hands",
            "He couldn't even ride a bike",
            "He couldn't even dance",
            "With the girl that he liked",
            "He lived in tiny villages",
            "And prayed to tiny god",
            "He couldn't go to gameshow",
            "Cause he could not applaud...",
        ]
        url = reverse('api:bot:mailinglist-seen-items', args=(self.list.name,))
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["The request body must be a string"]
        })


class MailingListWithSeenItemsTests(AuthenticatedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list = MailingList.objects.create(name='erlang-dev')
        cls.seen_item = MailingListSeenItem.objects.create(hash='12345', list=cls.list)

    def test_get_mailing_list(self):
        url = reverse('api:bot:mailinglist-detail', args=(self.list.name,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': self.list.id, 'name': self.list.name, 'seen_items': [self.seen_item.hash]
        })

    def test_prevents_duplicate_addition_of_seen_item(self):
        url = reverse('api:bot:mailinglist-seen-items', args=(self.list.name,))
        response = self.client.post(url, data=self.seen_item.hash)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Seen item already known."]
        })
