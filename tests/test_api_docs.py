import os
import json
from tests import SiteTest, app

class ApiBotUsersEndpoint(SiteTest):
    def test_api_docs(self):
        """ Check documentation metadata API """
        bad_data = json.dumps({'package': 'whatever', 'correct format': False})
        valid_data = {
            'package': "lemonapi",
            'base_url': "http://example.com/",
            'inventory_url': "http://example.com/object.inv"
        }
        valid_data_json = json.dumps(valid_data)
        unknown_package_json = json.dumps({'package': "whatever"})
        delete_data_json = json.dumps({'package': valid_data['package']})

        # GET - all entries
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

        # GET - unknown package
        response = self.client.get('/docs?package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

        # GET - multiple unknown packages
        response = self.client.get('/docs?package=whatever&package=everwhat', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

        # POST - no data
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

        # POST - malformed data
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=bad_data)
        self.assertEqual(response.status_code, 400)

        # POST - valid data
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=valid_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

        # GET - added package in all entries
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_data, response.json)

        # GET - added package detail
        response = self.client.get(
            f'/docs?package={valid_data["package"]}', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [valid_data])

        # GET - added package is the only package for query with another unknown package
        response = self.client.get(
            f'/docs?package={valid_data["package"]}&package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [valid_data])

        # DELETE - missing request body
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

        # DELETE - unknown package
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=unknown_package_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 0)

        # DELETE - added package
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=delete_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 1)

        # GET - added package is no longer in all entries
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(valid_data, response.json)
