from django.contrib.auth.models import User
from rest_framework.test import APITestCase


test_user, _created = User.objects.get_or_create(
    username='test',
    email='test@example.com',
    password='testpass',
    is_superuser=True,
    is_staff=True
)


class APISubdomainTestCase(APITestCase):
    """
    Configures the test client.

    This ensures that it uses the proper subdomain for requests, and forces authentication
    for the test user.

    The test user is considered staff and superuser.
    If you want to test for a custom user (for example, to test model permissions),
    create the user, assign the relevant permissions, and use
    `self.client.force_authenticate(user=created_user)` to force authentication
    through the created user.

    Using this performs the following niceties for you which ease writing tests:
    - setting the `HTTP_HOST` request header to `api.pythondiscord.local:8000`, and
    - forcing authentication for the test user.
    If you don't want to force authentication (for example, to test a route's response
    for an unauthenticated user), un-force authentication by using the following:

    >>> from pydis_site.apps.api.tests.base import APISubdomainTestCase
    >>> class UnauthedUserTestCase(APISubdomainTestCase):
    ...     def setUp(self):
    ...         super().setUp()
    ...         self.client.force_authentication(user=None)
    ...     def test_can_read_objects_at_my_endpoint(self):
    ...         resp = self.client.get('/my-publicly-readable-endpoint')
    ...         self.assertEqual(resp.status_code, 200)
    ...     def test_cannot_delete_objects_at_my_endpoint(self):
    ...         resp = self.client.delete('/my-publicly-readable-endpoint/42')
    ...         self.assertEqual(resp.status_code, 401)

    Make sure to include the `super().setUp(self)` call, otherwise, you may get
    status code 404 for some URLs due to the missing `HTTP_HOST` header.

    ## Example
    Using this in a test case is rather straightforward:

    >>> from pydis_site.apps.api.tests.base import APISubdomainTestCase
    >>> class MyAPITestCase(APISubdomainTestCase):
    ...     def test_that_it_works(self):
    ...         response = self.client.get('/my-endpoint')
    ...         self.assertEqual(response.status_code, 200)

    To reverse URLs of the API host, you need to use `django_hosts`:

    >>> from django_hosts.resolvers import reverse
    >>> from pydis_site.apps.api.tests.base import APISubdomainTestCase
    >>> class MyReversedTestCase(APISubdomainTestCase):
    ...     def test_my_endpoint(self):
    ...         url = reverse('user-detail', host='api')
    ...         response = self.client.get(url)
    ...         self.assertEqual(response.status_code, 200)
    """

    def setUp(self):
        super().setUp()
        self.client.defaults['HTTP_HOST'] = 'api.pythondiscord.local:8000'
        self.client.force_authenticate(test_user)
