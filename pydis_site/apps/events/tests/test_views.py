from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django_hosts.resolvers import reverse


PAGES_PATH = Path(settings.BASE_DIR, "pydis_site", "templates", "events", "test-pages")


class IndexTests(TestCase):
    def test_events_index_response_200(self):
        """Should return response code 200 when visiting index of events."""
        url = reverse("events:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class PageTests(TestCase):
    @override_settings(EVENTS_PAGES_PATH=PAGES_PATH)
    def test_valid_event_page_reponse_200(self):
        """Should return response code 200 when visiting valid event page."""
        pages = (
            reverse("events:page", ("my-event",)),
            reverse("events:page", ("my-event/subpage",)),
        )
        for page in pages:
            with self.subTest(page=page):
                resp = self.client.get(page)
                self.assertEqual(resp.status_code, 200)

    @override_settings(EVENTS_PAGES_PATH=PAGES_PATH)
    def test_invalid_event_page_404(self):
        """Should return response code 404 when visiting invalid event page."""
        pages = (
            reverse("events:page", ("invalid",)),
            reverse("events:page", ("invalid/invalid",))
        )
        for page in pages:
            with self.subTest(page=page):
                resp = self.client.get(page)
                self.assertEqual(resp.status_code, 404)
