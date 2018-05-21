import json
import pytest
from tests import SiteTest, app

class ApiDocsEndpoint(SiteTest):
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

    @pytest.mark.run(order=1)
    def test_api_docs_get_all(self):
        """ GET - all entries """
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    @pytest.mark.run(order=2)
    def test_api_docs_get_unknown(self):
        """ GET - unknown package """
        response = self.client.get('/docs?package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @pytest.mark.run(order=3)
    def test_api_docs_get_multi_unknown(self):
        """ GET - multiple unknown packages """
        response = self.client.get('/docs?package=whatever&package=everwhat', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    @pytest.mark.run(order=4)
    def test_api_docs_post_no_data(self):
        """ POST - no data """
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=5)
    def test_api_docs_post_bad_data(self):
        """ POST - malformed data """
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.bad_data)
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=6)
    def test_api_docs_post_good_data(self):
        """ POST - valid data """
        response = self.client.post('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.valid_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

    @pytest.mark.run(order=7)
    def test_api_docs_get_valid(self):
        """ GET - added package in all entries """
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.valid_data, response.json)

    @pytest.mark.run(order=8)
    def test_api_docs_get_detail(self):
        """ GET - added package detail """
        response = self.client.get(
            f'/docs?package={self.valid_data["package"]}', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [self.valid_data])

    @pytest.mark.run(order=9)
    def test_api_docs_get_partly_known(self):
        """ GET - added package is the only package for query with another unknown package """
        response = self.client.get(
            f'/docs?package={self.valid_data["package"]}&package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [self.valid_data])

    @pytest.mark.run(order=10)
    def test_api_docs_delete_bad(self):
        """ DELETE - missing request body """
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=11)
    def test_api_docs_delete_unknown(self):
        """ DELETE - unknown package """
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.unknown_package_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 0)

    @pytest.mark.run(order=12)
    def test_api_docs_delete_all(self):
        """ DELETE - added package """
        response = self.client.delete('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.delete_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 1)

    @pytest.mark.run(order=13)
    def test_api_docs_get_missing(self):
        """ GET - added package is no longer in all entries """
        response = self.client.get('/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.valid_data, response.json)
