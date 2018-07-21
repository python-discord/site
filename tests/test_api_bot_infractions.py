import json

from tests import SiteTest, app

TEST_USER_ID = "test"


class ApiBotInfractionsEndpoint(SiteTest):

    def test_infraction_create_invalid(self):
        # Invalid infraction type
        post_data_invalid_type = json.dumps(
            {"type": "not_a_type", "reason": "test", "user_id": TEST_USER_ID, "actor_id": TEST_USER_ID}
        )
        response = self.client.post("/bot/infractions", app.config["API_SUBDOMAIN"],
                                    headers=app.config["TEST_HEADER"],
                                    data=post_data_invalid_type)
        self.assert400(response)

    def test_infraction_kick(self):
        post_data_valid = json.dumps(
            {"type": "kick", "reason": "test", "user_id": TEST_USER_ID, "actor_id": TEST_USER_ID}
        )
        response = self.client.post("/bot/infractions", app.config["API_SUBDOMAIN"],
                                    headers=app.config["TEST_HEADER"],
                                    data=post_data_valid)
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertTrue("id" in response.json["infraction"])
        infraction_id = response.json["infraction"]["id"]
        response = self.client.get(f"/bot/infractions/id/{infraction_id}", app.config["API_SUBDOMAIN"],
                                   headers=app.config["TEST_HEADER"])
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertTrue("id" in response.json["infraction"])
        self.assertEqual(response.json["infraction"]["id"], infraction_id)
        self.assertTrue("active" in response.json["infraction"])
        self.assertFalse(response.json["infraction"]["active"])

    def test_infraction_ban(self):
        post_data_valid = json.dumps(
            {"type": "ban", "reason": "baddie", "user_id": TEST_USER_ID, "actor_id": TEST_USER_ID}
        )
        response = self.client.post("/bot/infractions", app.config["API_SUBDOMAIN"],
                                    headers=app.config["TEST_HEADER"],
                                    data=post_data_valid)
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertTrue("id" in response.json["infraction"])
        infraction_id = response.json["infraction"]["id"]

        # Check if the ban is currently applied
        response = self.client.get(f"/bot/infractions/user/{TEST_USER_ID}/ban/current", app.config["API_SUBDOMAIN"],
                                   headers=app.config["TEST_HEADER"])
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertIsNotNone(response.json["infraction"])
        self.assertTrue("id" in response.json["infraction"])
        self.assertEqual(response.json["infraction"]["id"], infraction_id)
        self.assertIsNone(response.json["infraction"]["expires_at"])
        self.assertTrue(response.json["infraction"]["active"])

        # Update the expiration to 1d
        patch_data_valid = json.dumps(
            {"id": infraction_id, "duration": "1d"}
        )
        response = self.client.patch("/bot/infractions", app.config["API_SUBDOMAIN"],
                                     headers=app.config["TEST_HEADER"],
                                     data=patch_data_valid)
        self.assert200(response)
        self.assertTrue("success" in response.json)
        self.assertTrue("infraction" in response.json)
        self.assertTrue(response.json["success"])
        self.assertIsNotNone(response.json["infraction"]["expires_at"])
        self.assertTrue(response.json["infraction"]["active"])

        # Disable the ban
        patch_data_valid = json.dumps(
            {"id": infraction_id, "active": False}
        )
        response = self.client.patch("/bot/infractions", app.config["API_SUBDOMAIN"],
                                     headers=app.config["TEST_HEADER"],
                                     data=patch_data_valid)
        self.assert200(response)
        self.assertTrue("success" in response.json)
        self.assertTrue("infraction" in response.json)
        self.assertTrue(response.json["success"])
        self.assertFalse(response.json["infraction"]["active"])

        # Check if there is no active ban anymore
        response = self.client.get(f"/bot/infractions/user/{TEST_USER_ID}/ban/current", app.config["API_SUBDOMAIN"],
                                   headers=app.config["TEST_HEADER"])
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertIsNone(response.json["infraction"])

        # Re-activate the ban
        patch_data_valid = json.dumps(
            {"id": infraction_id, "active": True}
        )
        response = self.client.patch("/bot/infractions", app.config["API_SUBDOMAIN"],
                                     headers=app.config["TEST_HEADER"],
                                     data=patch_data_valid)
        self.assert200(response)
        self.assertTrue("success" in response.json)
        self.assertTrue("infraction" in response.json)
        self.assertTrue(response.json["success"])
        self.assertTrue(response.json["infraction"]["active"])

        # Create a new ban
        post_data_valid = json.dumps(
            {"type": "ban", "reason": "baddie v2.0", "user_id": TEST_USER_ID, "actor_id": TEST_USER_ID}
        )
        response = self.client.post("/bot/infractions", app.config["API_SUBDOMAIN"],
                                    headers=app.config["TEST_HEADER"],
                                    data=post_data_valid)
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertTrue("id" in response.json["infraction"])
        new_infraction_id = response.json["infraction"]["id"]

        # Check if the old ban is now disabled
        response = self.client.get(f"/bot/infractions/id/{infraction_id}", app.config["API_SUBDOMAIN"],
                                   headers=app.config["TEST_HEADER"])
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertFalse(response.json["infraction"]["active"])

        # Check if the current ban infraction is the new infraction
        response = self.client.get(f"/bot/infractions/user/{TEST_USER_ID}/ban/current", app.config["API_SUBDOMAIN"],
                                   headers=app.config["TEST_HEADER"])
        self.assert200(response)
        self.assertTrue("infraction" in response.json)
        self.assertEqual(response.json["infraction"]["id"], new_infraction_id)
