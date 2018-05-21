import os
from tests import SiteTest, app

class WikiEndpoints(SiteTest):
    """ Test cases for the wiki subdomain """
    def test_wiki_edit(self):
        """Test that the wiki edit page redirects to login"""
        response = self.client.get("/edit/page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)

    def test_wiki_edit_post_empty_request(self):
        """Empty request should redirect to login"""
        response = self.client.post("/edit/page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 302)

    def test_wiki_history(self):
        """Test the history show"""
        response = self.client.get("/history/show/blahblah-non-existant-page", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 404) # Test that unknown routes 404

    def test_wiki_diff(self):
        """Test whether invalid revision IDs error"""
        response = self.client.get("/history/compare/ABC/XYZ", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 404) # Test that unknown revisions 404

    def test_wiki_special(self):
        """Test whether invalid revision IDs error"""
        response = self.client.get("/special", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 200)

    def test_wiki_special_all_pages(self):
        """Test whether invalid revision IDs error"""
        response = self.client.get("/special/all_pages", app.config['WIKI_SUBDOMAIN'])
        self.assertEqual(response.status_code, 200)
