import os
import json
from tests import SiteTest, app

class ApiBotUsersEndpoint(SiteTest):
    def test_api_user(self):
        """ Check insert user """

        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        single_data = json.dumps({'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000"})
        list_data = json.dumps([{'user_id': "1234", 'roles': ["5678"], "username": "test", "discriminator": "0000"}])

        response = self.client.get('/bot/users', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 405)

        response = self.client.post('/bot/users', app.config['API_SUBDOMAIN'], headers=headers, data=single_data)
        self.assertTrue("inserted" in response.json)

        response = self.client.post('/bot/users', app.config['API_SUBDOMAIN'], headers=headers, data=list_data)
        self.assertTrue("inserted" in response.json)
