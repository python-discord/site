"""Tests the `/api/bot/snake_` endpoints."""

from tests import SiteTest, app


class TestSnakeFactsAPI(SiteTest):
    """GET method - get snake fact"""

    def test_snake_facts(self):
        response = self.client.get(
            '/bot/snake_facts',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)


class TestSnakeIdiomAPI(SiteTest):
    """GET method - get snake idiom"""

    def test_snake_idiom(self):
        response = self.client.get(
            '/bot/snake_idioms',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), str)


class TestSnakeQuizAPI(SiteTest):
    """GET method - get snake quiz"""

    def test_snake_quiz(self):
        response = self.client.get(
            '/bot/snake_quiz',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)


class TestSnakeNameAPI(SiteTest):
    """GET method - get a single snake name, or all of them."""

    def test_snake_names(self):
        response = self.client.get(
            '/bot/snake_names',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), dict)

    def test_snake_names_all(self):
        response = self.client.get(
            '/bot/snake_names?get_all=True',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), list)
