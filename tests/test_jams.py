from tests import SiteTest, app

class JamsEndpoint(SiteTest):
    """ Test cases for the root endpoint and error handling """

    def test_jams_page(self):
        """ Check the jams path responds with 200 OK """
        response = self.client.get('/jams', 'http://'+app.config['SERVER_NAME'])
        self.assertEqual(response.status_code, 200)


