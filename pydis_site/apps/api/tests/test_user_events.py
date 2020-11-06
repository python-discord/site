from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import User, UserEvent


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            id=1,
            name="I am a user.",
            discriminator=1,
            in_guild=True
        )
        cls.user_event = UserEvent.objects.create(
            name="Setup Event",
            organizer=cls.user1,
            description="A test event",
            message_id=1
        )

    def test_returns_201_for_created_user_event(self):
        url = reverse("bot:userevent-list", host="api")
        data = {
            "name": "Test Event",
            "organizer": self.user1.id,
            "description": "A test event",
            "message_id": 2,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

    def test_returns_400_for_existing_user_event_name(self):
        url = reverse("bot:userevent-list", host="api")
        data = {
            "name": "Setup Event",
            "organizer": self.user1.id,
            "description": "A test event",
            "message_id": 3,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_invalid_user_ids(self):
        url = reverse("bot:userevent-list", host="api")
        data = {
            "name": "Invalid Event",
            "organizer": 23243654,
            "description": "A test event",
            "message_id": 5,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_invalid_event_name(self):
        url = reverse("bot:userevent-list", host="api")
        data = {
            "name": (
                "Sit ut ea dolore non ad ad do eu ut "
                "consectetur irure nisi labore elit "
                "fugiat et ut id mollit sit fugiat "
                "velit veniam veniam elit."
            ),
            "organizer": self.user1.id,
            "description": "A test event",
            "message_id": 6,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_non_unique_message_id(self):
        url = reverse("bot:userevent-list", host="api")
        data = {
            "name": "Random Invalid Event",
            "organizer": self.user1.id,
            "description": "A test event",
            "message_id": 1,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)


class UpdateTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            id=1,
            name="I am a user.",
            discriminator=1,
            in_guild=True
        )
        cls.user2 = User.objects.create(
            id=2,
            name="I am a user 2.",
            discriminator=1,
            in_guild=True
        )
        cls.user_event = UserEvent.objects.create(
            name="Patch me",
            organizer=cls.user1,
            description="A test event",
            message_id=100
        )

    def test_returns_200_for_patching_user_event(self):
        url = reverse("bot:userevent-detail", host="api", args=(self.user_event.name,))
        data = {
            "description": "This is the new description."
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], data["description"])

    def test_returns_400_for_invalid_organizer_id(self):
        url = reverse("bot:userevent-detail", host="api", args=(self.user_event.name,))
        data = {
            "organizer": 23243654,
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 400)


class FilterTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            id=1,
            name="I am a user.",
            discriminator=1,
            in_guild=True
        )
        cls.user2 = User.objects.create(
            id=2,
            name="I am a user 2.",
            discriminator=1,
            in_guild=True
        )
        cls.user_event = UserEvent.objects.create(
            name="Patch me",
            organizer=cls.user1,
            description="A test event",
            message_id=101
        )

    def test_organizer_filter(self):
        url = reverse("bot:userevent-list", host="api")
        params = {
            "organizer": 1
        }
        response = self.client.get(url, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["organizer"], params["organizer"])
