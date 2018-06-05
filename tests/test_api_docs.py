import json

from tests import SiteTest, app


class ApiDocsEndpoint(SiteTest):
    """ Check documentation metadata API """

    bad_data = json.dumps({'package': 'whatever', 'correct format': False})
    unknown_package_json = json.dumps({'package': "whatever"})

    def test_api_docs_get_all(self):
        """ GET - all entries """
        response = self.client.get('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_api_docs_get_unknown(self):
        """ GET - unknown package """
        response = self.client.get('/bot/docs?package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_api_docs_get_multi_unknown(self):
        """ GET - multiple unknown packages """
        response = self.client.get('/bot/docs?package=whatever&package=everwhat', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_api_docs_post_no_data(self):
        """ POST - no data """
        response = self.client.post('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

    def test_api_docs_post_bad_data(self):
        """ POST - malformed data """
        response = self.client.post('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.bad_data)
        self.assertEqual(response.status_code, 400)

    def test_api_docs_delete_bad(self):
        """ DELETE - missing request body """
        response = self.client.delete('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

    def test_api_docs_delete_unknown(self):
        """ DELETE - unknown package """
        response = self.client.delete('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.unknown_package_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 0)


class SinglePackageApiDocsEndpointTests(SiteTest):
    """ Test the API docs endpoint with a single package added """

    valid_data = {
        'package': "lemonapi",
        'base_url': "http://example.com/",
        'inventory_url': "http://example.com/object.inv"
    }
    delete_data_json = json.dumps({'package': valid_data['package']})
    valid_data_json = json.dumps(valid_data)

    def setUp(self):
        """ POST valid data to the server for use in this test case """
        response = self.client.post('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.valid_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

    def test_api_docs_get_valid(self):
        """ GET - added package is in all entries """
        response = self.client.get('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.valid_data, response.json)

    def test_api_docs_get_detail(self):
        """ GET - added package detail """
        response = self.client.get(
            f'/bot/docs?package={self.valid_data["package"]}', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [self.valid_data])

    def test_api_docs_get_partly_known(self):
        """ GET - added package is the only package for query with another unknown package """
        response = self.client.get(
            f'/bot/docs?package={self.valid_data["package"]}&package=whatever', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [self.valid_data])

    def test_api_docs_delete_all(self):
        """ DELETE - added package """
        response = self.client.delete('/bot/docs', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=self.delete_data_json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deleted'], 1)
