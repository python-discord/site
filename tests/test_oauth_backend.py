from tests import SiteTest, manager

class TestOAuthBackend(SiteTest):
    """ Test cases for the oauth.py file """

    def test_get(self):
        """ Make sure the get function returns nothing """
        self.assertIsNone(manager.oauth_backend.get())

    def test_delete(self):
        """ Make sure the delete function returns nothing """
        self.assertIsNone(manager.oauth_backend.delete(None))

    def test_logout(self):
        """ Make sure at least apart of logout is working :/ """
        self.assertIsNone(manager.oauth_backend.logout())

    def test_add_user(self):
        """ Make sure function adds values to database and session """
        from flask import session

        from pysite.constants import OAUTH_DATABASE

        sess_id = "hey bro wazup"
        fake_token = {"access_token": "access_token", "id": sess_id, "refresh_token": "refresh_token", "expires_at": 5}
        fake_user = {"id": 1235678987654321, "username": "Zwacky", "discriminator": "#6660"}
        manager.db.conn = manager.db.get_connection()
        manager.oauth_backend.add_user(fake_token, fake_user, sess_id)

        self.assertEqual(sess_id, session["session_id"])
        fake_token["snowflake"] = fake_user["id"]
        fake_user["user_id"] = fake_user["id"]
        del fake_user["id"]
        self.assertEqual(fake_token, manager.db.get(OAUTH_DATABASE, sess_id))
        self.assertEqual(fake_user, manager.db.get("users", fake_user["user_id"]))

        manager.db.delete(OAUTH_DATABASE, sess_id)
        manager.db.delete("users", fake_user["user_id"])
        manager.db.teardown_request(None)
