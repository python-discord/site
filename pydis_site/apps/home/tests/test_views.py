from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import TestCase
from django_hosts.resolvers import get_host, reverse, reverse_host


def check_redirect_url(
        response: HttpResponseRedirect, reversed_url: str, strip_params=True
) -> bool:
    """
    Check whether a given redirect response matches a specific reversed URL.

    Arguments:
    * `response`: The HttpResponseRedirect returned by the test client
    * `reversed_url`: The URL returned by `reverse()`
    * `strip_params`: Whether to strip URL parameters (following a "?") from the URL given in the
                     `response` object
    """
    host = get_host(None)
    hostname = reverse_host(host)

    redirect_url = response.url

    if strip_params and "?" in redirect_url:
        redirect_url = redirect_url.split("?", 1)[0]

    result = reversed_url == f"//{hostname}{redirect_url}"
    return result


class TestAccountDeleteView(TestCase):
    def setUp(self) -> None:
        """Create an authorized Django user for testing purposes."""
        self.user = User.objects.create(
            username="user#0000"
        )

    def test_redirect_when_logged_out(self):
        """Test that the user is redirected to the homepage when not logged in."""
        url = reverse("account_delete")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, reverse("home")))

    def test_get_when_logged_in(self):
        """Test that the view returns a HTTP 200 when the user is logged in."""
        url = reverse("account_delete")

        self.client.force_login(self.user)
        resp = self.client.get(url)
        self.client.logout()

        self.assertEqual(resp.status_code, 200)

    def test_post_invalid(self):
        """Test that the user is redirected when the form is filled out incorrectly."""
        url = reverse("account_delete")

        self.client.force_login(self.user)

        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, url))

        resp = self.client.post(url, {"username": "user"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, url))

        self.client.logout()

    def test_post_valid(self):
        """Test that the account is deleted when the form is filled out correctly.."""
        url = reverse("account_delete")

        self.client.force_login(self.user)

        resp = self.client.post(url, {"username": "user#0000"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, reverse("home")))

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=self.user.username)

        self.client.logout()


class TestAccountSettingsView(TestCase):
    def setUp(self) -> None:
        """Create an authorized Django user for testing purposes."""
        self.user = User.objects.create(
            username="user#0000"
        )

    def test_redirect_when_logged_out(self):
        """Check that the user is redirected to the homepage when not logged in."""
        url = reverse("account_settings")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, reverse("home")))

    def test_get_when_logged_in(self):
        """Test that the view returns a HTTP 200 when the user is logged in."""
        url = reverse("account_settings")

        self.client.force_login(self.user)
        resp = self.client.get(url)
        self.client.logout()

        self.assertEqual(resp.status_code, 200)


class TestIndexReturns200(TestCase):
    def test_index_returns_200(self):
        """Check that the index page returns a HTTP 200 response."""
        url = reverse('home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class TestLoginCancelledReturns302(TestCase):
    def test_login_cancelled_returns_302(self):
        """Check that the login cancelled redirect returns a HTTP 302 response."""
        url = reverse('socialaccount_login_cancelled')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, reverse("home")))


class TestLoginErrorReturns302(TestCase):
    def test_login_error_returns_302(self):
        """Check that the login error redirect returns a HTTP 302 response."""
        url = reverse('socialaccount_login_error')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(check_redirect_url(resp, reverse("home")))
