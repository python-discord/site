from django.conf import settings
from django.test import TestCase
from django.urls import reverse

TESTING_ARGUMENTS = {"resources_resources_redirect": ("reading",)}


class RedirectTests(TestCase):
    """Survival tests for redirects."""

    def test_redirects(self) -> None:
        """
        Should redirect to given route based on redirect rules.

        Makes sure that every redirect:
        1. Redirects only once.
        2. Redirects to right URL.
        """
        for original_path, (redirect_route, name, static_args) in settings.REDIRECTIONS.items():
            with self.subTest(
                    original_path=original_path,
                    redirect_route=redirect_route,
                    name=name,
                    static_args=static_args,
                    args=TESTING_ARGUMENTS.get(name, ())
            ):
                resp = self.client.get(
                    reverse(
                        f"home:redirect:{name}",
                        args=TESTING_ARGUMENTS.get(name, ())
                    ),
                    follow=True
                )

                self.assertEqual(1, len(resp.redirect_chain))
                self.assertRedirects(
                    resp,
                    reverse(
                        f"home:{redirect_route}",
                        args=TESTING_ARGUMENTS.get(name, ()) + static_args
                    ),
                    status_code=301
                )
