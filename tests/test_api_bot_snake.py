import os
from tests import SiteTest, app

class ApiBotSnakeEndpoints(SiteTest):
    """
    Tests the following endpoints:
        - snake_movies
        - snake_quiz
        - snake_names
        - snake_idioms
        - snake_facts
    """

    def test_snake_facts(self):
        # GET method - get snake fact
        response = self.client.get('/bot/snake_facts', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)

    def test_snake_idiom(self):
        # GET method - get snake idiom
        response = self.client.get('/bot/snake_idioms', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)

    def test_snake_quiz(self):
        # GET method - get snake quiz
        response = self.client.get('/bot/snake_quiz', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)

    def test_snake_names(self):
        # GET method - get snake name
        response = self.client.get('/bot/snake_names', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)

    def test_snake_names_all(self):
        # GET method - get all snake names
        response = self.client.get('/bot/snake_names?get_all=True', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), list)
