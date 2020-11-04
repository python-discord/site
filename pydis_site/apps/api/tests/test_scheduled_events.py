from datetime import datetime, timedelta

from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import ScheduledEvent, User, UserEvent


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(
            id=1,
            name="I am a user 1",
            discriminator=1,
            in_guild=True
        )
        cls.user_2 = User.objects.create(
            id=2,
            name="I am a user 2",
            discriminator=1,
            in_guild=True
        )
        cls.user_event_1 = UserEvent.objects.create(
            name="User Event 1",
            organizer=cls.user_1,
            description="Some desc",
            message_id=1
        )

        cls.user_event_2 = UserEvent.objects.create(
            name="User Event 2",
            organizer=cls.user_1,
            description="Some desc",
            message_id=2
        )
        cls.user_event_3 = UserEvent.objects.create(
            name="User Event 3",
            organizer=cls.user_2,
            description="Some desc",
            message_id=3
        )
        cls.scheduled_event = ScheduledEvent.objects.create(
            user_event=cls.user_event_1,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=3)
        )

    def test_returns_201_for_scheduled_user_event(self):
        url = reverse("bot:scheduledevent-list", host="api")
        start = datetime.now() + timedelta(days=1)
        data = {
            "user_event_name": self.user_event_3.name,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(hours=3)).isoformat()
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_returns_400_for_invalid_user_event(self):
        url = reverse("bot:scheduledevent-list", host="api")

        data = {
            "user_event": "Non existent",
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=3)).isoformat()
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_overlapping_time_slots(self):
        """Return 400 if the new event time(s) clash/overlap with an already scheduled event."""
        url = reverse("bot:scheduledevent-list", host="api")
        data = {
            "user_event_name": self.user_event_3.name,
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=3)).isoformat()
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_user_scheduling_multiple_events(self):
        url = reverse("bot:scheduledevent-list", host="api")
        start = datetime.now() + timedelta(days=2)
        data = {
            "user_event_name": self.user_event_2.name,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(hours=3)).isoformat()
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_already_scheduled_event(self):
        url = reverse("bot:scheduledevent-list", host="api")
        start = datetime.now() + timedelta(days=3)
        data = {
            "user_event_name": self.user_event_1.name,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(hours=3)).isoformat()
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_short_event_duration(self):
        url = reverse("bot:scheduledevent-list", host="api")
        start = datetime.now() + timedelta(days=3)
        data = {
            "user_event_name": self.user_event_3.name,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=10)).isoformat()
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_for_extended_event_duration(self):
        url = reverse("bot:scheduledevent-list", host="api")
        start = datetime.now() + timedelta(days=3)
        data = {
            "user_event_name": self.user_event_3.name,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(hours=6)).isoformat()
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
