import os
import json
from tests import SiteTest, app

class RstEndpoints(SiteTest):
    """ Test cases for staff subdomain """

    def test_staff_view(self):
        """ Check staff view redirects """
        response = self.client.get('/', "http://"+app.config['SERVER_NAME'])
        self.assertEqual(response.status_code, 200)
