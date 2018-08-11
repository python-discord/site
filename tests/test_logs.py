"""Tests the `/api/bot/clean` endpoint."""
import json

from tests import SiteTest, app


class TestCleanLogAPI(SiteTest):
    """
    Tests submitting a clean log and
    verifies that we get a UUID in return.

    Also ensures that we get a 400 if we send in bad data.
    """

    def test_returns_400_on_bad_data(self):
        bad_data = json.dumps({
            "scubfire": "testiclaes"
        })

        response = self.client.post(
            '/bot/logs',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER'],
            data=bad_data
        )
        self.assert400(response)

    def test_submit_clean_log(self):
        good_data = json.dumps({
            "log_data": [
                {
                    "author": "something",
                    "user_id": "12345151",
                    "role_id": "4818413",
                    "content": "testy",
                    "timestamp": "this way comes",
                    "embeds": [{"fire":"nanny"}],
                    "attachments": ["<Attachment>"],
                }
            ]
        })

        response = self.client.post(
            '/bot/logs',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER'],
            data=good_data
        )

        log_id = response.json.get("log_id")

        self.assert200(response)
        self.assertIsNotNone(log_id)
        self.assertGreater(len(log_id), 2)
        self.assertEqual(type(log_id), str)


class TestCleanLogFrontEnd(SiteTest):
    """
    Tests the frontend for
    viewing the clean logs.

    Best I can do with our current
    system is check if I'm redirected,
    since this is behind OAuth.
    """

    def test_clean_log_frontend_returns_302(self):
        response = self.client.get(
            f'/bot/logs/1',
            'http://pytest.local'
        )

        self.assertEqual(response.status_code, 302)