from app import app

from flask_testing import TestCase


class SiteTest(TestCase):
    ''' extend TestCase with flask app instantiation '''
    def create_app(self):
        ''' add flask app configuration settings '''
        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.allow_subdomain_redirects = True
        return app


class RootEndpoint(SiteTest):
    ''' test cases for the root endpoint and error handling '''
    def test_index(self):
        ''' Check the root path reponds with 200 OK '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        ''' Check paths without handlers returns 404 Not Found '''
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)
