from tests import SiteTest
from pysite.constants import DISCORD_OAUTH_REDIRECT
from pysite.constants import DISCORD_OAUTH_AUTHORIZED
from pysite.constants import ERROR_DESCRIPTIONS


class RootEndpoint(SiteTest):
    """ Test cases for the root endpoint and error handling """

    def test_index(self):
        """ Check the root path responds with 200 OK """
        response = self.client.get('/', 'http://pytest.local')
        self.assertEqual(response.status_code, 200)

    def test_info_index(self):
        """ Check the info index path responds with a 301 """
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 301)

    def test_info_help(self):
        """ Check the info help path responds with 200 OK """
        response = self.client.get('/info/help')
        self.assertEqual(response.status_code, 200)

    def test_info_resources(self):
        """ Check the info resources path responds with 200 OK """
        response = self.client.get('/info/resources')
        self.assertEqual(response.status_code, 200)

    def test_info_resources_json(self):
        """ Check the resources JSON loads correctly """
        response = self.client.get('/static/resources.json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    def test_info_rules(self):
        """ Check the info rules path responds with 200 OK """
        response = self.client.get('/info/help')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        """ Check paths without handlers returns 404 Not Found """
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)

    def test_error(self):
        """ Check the error pages """
        for code in ERROR_DESCRIPTIONS.keys():
            response = self.client.get(f'/error/{code}')
            self.assertEqual(response.status_code, code)

    def test_invite(self):
        """ Check invite redirects """
        response = self.client.get('/invite')
        self.assertEqual(response.status_code, 302)

    def test_ws_test(self):
        """ Check ws_test responds """
        response = self.client.get('/ws_test')
        self.assertEqual(response.status_code, 200)

    def test_oauth_redirects(self):
        """ Check oauth redirects """
        response = self.client.get(DISCORD_OAUTH_REDIRECT)
        self.assertEqual(response.status_code, 302)

    def test_oauth_logout(self):
        """ Check oauth redirects """
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 302)

    def test_oauth_authorized(self):
        """ Check oauth authorization """
        response = self.client.get(DISCORD_OAUTH_AUTHORIZED)
        self.assertEqual(response.status_code, 302)

    def test_stats_redirect(self):
        """ Check stats path redirects """
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 302)

    def test_500_easter_egg(self):
        """ Check the status of the /500 page"""
        response = self.client.get("/500")
        self.assertEqual(response.status_code, 500)
