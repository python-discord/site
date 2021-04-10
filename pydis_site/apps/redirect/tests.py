from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class RedirectTests(TestCase):
    def test_redirects(self):
        """
        Should redirect to given route based on redirect rules.

        Makes sure that every redirect:
        1. Redirects only once.
        2. Redirects to right URL.
        """
        for original_path, (redirect_route, name, args) in settings.REDIRECTIONS.items():
            with self.subTest(original_path=original_path, redirect_route=redirect_route, name=name, args=args):
                resp = self.client.get(reverse(f"home:redirect:{name}", args=args), follow=True)

                self.assertEqual(1, len(resp.redirect_chain))
                self.assertRedirects(resp, reverse(f"home:{redirect_route}", args=args))
