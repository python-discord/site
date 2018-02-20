import json  # pragma: no cover
import os  # pragma: no cover

from app import app

from flask_testing import TestCase  # pragma: no cover


class SiteTest(TestCase):
    ''' extend TestCase with flask app instantiation '''
    def create_app(self):
        ''' add flask app configuration settings '''
        server_name = 'pytest.local'
        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.config['SERVER_NAME'] = server_name
        app.config['API_SUBDOMAIN'] = f'http://api.{server_name}'
        app.config['STAFF_SUBDOMAIN'] = f'http://staff.{server_name}'
        app.allow_subdomain_redirects = True
        return app


class RootEndpoint(SiteTest):
    ''' test cases for the root endpoint and error handling '''
    def test_index(self):
        ''' Check the root path reponds with 200 OK '''
        response = self.client.get('/', 'http://pytest.local')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        ''' Check paths without handlers returns 404 Not Found '''
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)

    def test_invite(self):
        ''' Check invite redirects '''
        response = self.client.get('/invite')
        self.assertEqual(response.status_code, 302)

    def test_api_unknown_route(self):
        ''' Check api unknown route '''
        response = self.client.get('/', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'error_code': 0, 'error_message': 'Unknown API route'})
        self.assertEqual(response.status_code, 404)

    def test_api_healthcheck(self):
        ''' Check healthcheck url responds '''
        response = self.client.get('/healthcheck', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'status': 'ok'})
        self.assertEqual(response.status_code, 200)

    def test_api_tag(self):
        ''' Check tag api '''
        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        good_data = json.dumps({
            'tag_name': 'testing',
            'tag_content': 'testing',
            'tag_category': 'testing'})

        bad_data = json.dumps({
            'not_a_valid_key': 'testing',
            'tag_content': 'testing',
            'tag_category': 'testing'})

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(response.json, {'success': True})

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(response.json, [{'tag_name': 'testing'}])
        self.assertEqual(response.status_code, 200)

    def test_api_user(self):
        ''' Check insert user '''
        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        bad_data = json.dumps({'user_id': 1234, 'role': 5678})
        good_data = json.dumps([{'user_id': 1234, 'role': 5678}])

        response = self.client.get('/user', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 405)

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.json, {'error_code': 3, 'error_message': 'Incorrect parameters provided'})

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(True, "inserted" in response.json)
