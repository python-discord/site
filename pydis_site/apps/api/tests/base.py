from django.contrib.auth.models import User
from rest_framework.test import APITestCase


test_user, _created = User.objects.get_or_create(
    username='test',
    email='test@example.com',
    password='testpass',
    is_superuser=True,
    is_staff=True
)


class AuthenticatedAPITestCase(APITestCase):
    """
    Configures the test client.

    This ensures that it uses the proper subdomain for requests, and forces authentication
    for the test user.

    The test user is considered staff and superuser.
    If you want to test for a custom user (for example, to test model permissions),
    create the user, assign the relevant permissions, and use
    `self.client.force_authenticate(user=created_user)` to force authentication
    through the created user.

    Using this performs the following nicety for you which eases writing tests:
    - forcing authentication for the test user.
    If you don't want to force authentication (for example, to test a route's response
    for an unauthenticated user), un-force authentication by using the following:

    >>> from pydis_site.apps.api.tests.base import AuthenticatedAPITestCase
    >>> class UnauthedUserTestCase(AuthenticatedAPITestCase):
    ...     def setUp(self):
    ...         super().setUp()
    ...         self.client.force_authentication(user=None)
    ...     def test_can_read_objects_at_my_endpoint(self):
    ...         resp = self.client.get('/my-publicly-readable-endpoint')
    ...         self.assertEqual(resp.status_code, 200)
    ...     def test_cannot_delete_objects_at_my_endpoint(self):
    ...         resp = self.client.delete('/my-publicly-readable-endpoint/42')
    ...         self.assertEqual(resp.status_code, 401)

    ## Example
    Using this in a test case is rather straightforward:

    >>> from pydis_site.apps.api.tests.base import AuthenticatedAPITestCase
    >>> class MyAPITestCase(AuthenticatedAPITestCase):
    ...     def test_that_it_works(self):
    ...         response = self.client.get('/my-endpoint')
    ...         self.assertEqual(response.status_code, 200)

    To reverse URLs of the API host, you need to use `django.urls`:

    >>> from django.urls import reverse
    >>> from pydis_site.apps.api.tests.base import AuthenticatedAPITestCase
    >>> class MyReversedTestCase(AuthenticatedAPITestCase):
    ...     def test_my_endpoint(self):
    ...         url = reverse('api:user-detail')
    ...         response = self.client.get(url)
    ...         self.assertEqual(response.status_code, 200)
    """

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(test_user)
