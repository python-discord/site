from tests import SiteTest, app


class StaffEndpoints(SiteTest):
    """ Test cases for staff subdomain """

    def test_staff_view(self):
        """ Check staff view redirects """
        response = self.client.get('/', app.config['STAFF_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)

    def test_jams_infractions(self):
        """ Check staff jams infractions view redirects """
        response = self.client.get('/jams/infractions', app.config['STAFF_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)
