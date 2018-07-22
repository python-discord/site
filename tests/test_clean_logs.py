"""Tests the `/api/bot/clean` endpoint."""
import json

from tests import SiteTest, app


class TestCleanLogAPI(SiteTest):
    """
    Tests submitting a clean log and
    verifies that we get a UUID in return.

    Then tests that
    """

    def test_returns_400_on_bad_data(self):
        bad_data = json.dumps({
            "scubfire": "testiclaes"
        })

        response = self.client.post(
            '/bot/clean',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER'],
            data=bad_data
        )
        self.assert400(response)

    def test_submit_clean_log(self):
        good_data = json.dumps({
            "log_data": [
                {
                    "author":    "something",
                    "content":   "testy",
                    "timestamp": "this way comes"
                }
            ]
        })

        response = self.client.post(
            '/bot/clean',
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
    """

    def test_clean_log_frontend_returns_200(self):

        # Get a log ID
        good_data = json.dumps({
            "log_data": [
                {
                    "author":    "something",
                    "content":   "testy",
                    "timestamp": "this way comes"
                }
            ]
        })

        response = self.client.post(
            '/bot/clean',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER'],
            data=good_data
        )

        log_id = response.json.get("log_id")

        # Now try to access it.
        response = self.client.get(
            f'/bot/clean_logs/{log_id}'
        )

        self.assert200(response)
        self.assertIn("testy", response.text)