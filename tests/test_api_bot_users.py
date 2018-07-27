import json
from tests import SiteTest, app


class ApiBotUsersEndpoint(SiteTest):
    def test_api_user(self):
        """ Check insert user """
        single_data = json.dumps(
            {'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000", "avatar": "http://some/url"}
        )
        list_data = json.dumps([
            {'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000", "avatar": "http://some/url"}
        ])

        response = self.client.get('/bot/users?user_id=1234', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertTrue("data" in response.json)

        response = self.client.post('/bot/users', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=single_data)
        self.assertTrue("success" in response.json)

        response = self.client.post('/bot/users/complete', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=single_data)
        self.assertTrue("inserted" in response.json)

        response = self.client.post('/bot/users', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=list_data)
        self.assertTrue("success" in response.json)

        response = self.client.post('/bot/users/complete', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=list_data)
        self.assertTrue("inserted" in response.json)
