"""Tests the `/api/bot/off-topic-names` endpoint."""

from tests import SiteTest, app


class EmptyDatabaseOffTopicEndpointTests(SiteTest):
    """Tests fetching all entries from the endpoint with an empty database."""

    def test_get_returns_empty_list(self):
        response = self.client.get(
            '/bot/off-topic-names',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)
        self.assertEqual(response.json, [])


class AddingANameOffTopicEndpointTests(SiteTest):
    """Tests adding a channel name to the database."""

    def test_returns_400_on_bad_data(self):
        response = self.client.post(
            '/bot/off-topic-names?name=my%20TOTALLY%20VALID%20CHANNE%20NAME',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert400(response)

    def test_can_add_new_package(self):
        response = self.client.post(
            '/bot/off-topic-names?name=lemons-lemon-shop',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)


class AddingChannelNamesToDatabaseEndpointTests(SiteTest):
    """Tests fetching names from the database with GET."""

    CHANNEL_NAME = 'bisks-disks'

    def setUp(self):
        response = self.client.post(
            f'/bot/off-topic-names?name={self.CHANNEL_NAME}',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)

    def test_name_is_in_all_entries(self):
        response = self.client.get(
            '/bot/off-topic-names',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)
        self.assertIn(self.CHANNEL_NAME, response.json)


class AllowsNumbersInNames(SiteTest):
    """Tests that the site allows names with numbers in them."""

    def test_allows_numbers_in_names(self):
        response = self.client.post(
            f'/bot/off-topic-names?name=totallynot42',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)


class RandomSampleEndpointTests(SiteTest):
    """Tests fetching random names from the website with GET."""

    CHANNEL_NAME_1 = 'chicken-shed'
    CHANNEL_NAME_2 = 'robot-kindergarten'

    def setUp(self):
        response = self.client.post(
            f'/bot/off-topic-names?name={self.CHANNEL_NAME_1}',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)

        response = self.client.post(
            f'/bot/off-topic-names?name={self.CHANNEL_NAME_2}',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)

    def test_returns_limited_names_with_random_query_param(self):
        response = self.client.get(
            '/bot/off-topic-names?random_items=1',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)
        self.assertEqual(len(response.json), 1)


class DeletingANameEndpointTests(SiteTest):
    """Tests deleting a name from the database using DELETE."""

    CHANNEL_NAME = 'duck-goes-meow'

    def setUp(self):
        response = self.client.post(
            f'/bot/off-topic-names?name={self.CHANNEL_NAME}',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)

    def test_deleting_random_name_returns_deleted_0(self):
        response = self.client.delete(
            '/bot/off-topic-names?name=my-totally-random-name',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)
        self.assertEqual(response.json['deleted'], 0)

    def test_deleting_channel_name_returns_deleted_1(self):
        response = self.client.delete(
            f'/bot/off-topic-names?name={self.CHANNEL_NAME}',
            app.config['API_SUBDOMAIN'],
            headers=app.config['TEST_HEADER']
        )
        self.assert200(response)
        self.assertEqual(response.json['deleted'], 1)
