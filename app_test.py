#import pytest
#import json
from flask_testing import TestCase
from app import app

class siteTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.allow_subdomain_redirects = True
        return app


class RootEndpoint(siteTest):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api(self):
        from pprint import pprint
        response = self.client.get('/nonexistantpath')
        self.assertEqual(response.status_code, 404)
