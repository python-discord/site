from django_hosts.resolvers import reverse

from .base import APISubdomainTestCase
from ..models import Role


class CreationTests(APISubdomainTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admins_role = Role.objects.create(
            id=1,
            name="Admins",
            colour=1,
            permissions=1,
            position=4,
        )
        cls.developers_role = Role.objects.create(
            id=4,
            name="Helpers",
            colour=4,
            permissions=4,
            position=1,
        )
        cls.everyone_role = Role.objects.create(
            id=5,
            name="@everyone",
            colour=5,
            permissions=5,
            position=0,
        )
        cls.lowest_position_duplicate = Role.objects.create(
            id=6,
            name="lowest position duplicate",
            colour=6,
            permissions=6,
            position=0,
        )

    def _validate_roledict(self, role_dict: dict) -> None:
        """Helper method to validate a dict representing a role."""
        self.assertIsInstance(role_dict, dict)
        self.assertEqual(len(role_dict), 5)
        attributes = ('id', 'name', 'colour', 'permissions', 'position')
        self.assertTrue(all(attribute in role_dict for attribute in attributes))

    def test_role_ordering_lt(self):
        """Tests the __lt__ comparisons based on role position in the hierarchy."""
        self.assertTrue(self.everyone_role < self.developers_role)
        self.assertFalse(self.developers_role > self.admins_role)

    def test_role_ordering_le(self):
        """Tests the __le__ comparisons based on role position in the hierarchy."""
        self.assertTrue(self.everyone_role <= self.developers_role)
        self.assertTrue(self.everyone_role <= self.lowest_position_duplicate)
        self.assertTrue(self.everyone_role >= self.lowest_position_duplicate)
        self.assertTrue(self.developers_role >= self.everyone_role)

        self.assertFalse(self.developers_role >= self.admins_role)
        self.assertFalse(self.developers_role <= self.everyone_role)

    def test_role_min_max_ordering(self):
        """Tests the `min` and `max` operations based on the role hierarchy."""
        top_role_no_duplicates = max([self.developers_role, self.admins_role, self.everyone_role])
        self.assertIs(top_role_no_duplicates, self.admins_role)

        top_role_duplicates = max([self.developers_role, self.admins_role, self.admins_role])
        self.assertIs(top_role_duplicates, self.admins_role)

        bottom_role_no_duplicates = min(
            [self.developers_role, self.admins_role, self.everyone_role]
        )
        self.assertIs(bottom_role_no_duplicates, self.everyone_role)

        bottom_role_duplicates = min(
            [self.lowest_position_duplicate, self.admins_role, self.everyone_role]
        )
        self.assertIs(bottom_role_duplicates, self.lowest_position_duplicate)

    def test_role_list(self):
        """Tests the GET list-view and validates the contents."""
        url = reverse('bot:role-list', host='api')

        response = self.client.get(url)
        self.assertContains(response, text="id", count=4, status_code=200)

        roles = response.json()
        self.assertIsInstance(roles, list)
        self.assertEqual(len(roles), 4)

        for role in roles:
            self._validate_roledict(role)

    def test_role_get_detail_success(self):
        """Tests GET detail view of an existing role."""
        url = reverse('bot:role-detail', host='api', args=(self.admins_role.id, ))
        response = self.client.get(url)
        self.assertContains(response, text="id", count=1, status_code=200)

        role = response.json()
        self._validate_roledict(role)

        admins_role = Role.objects.get(id=role["id"])
        self.assertEqual(admins_role.name, role["name"])
        self.assertEqual(admins_role.colour, role["colour"])
        self.assertEqual(admins_role.permissions, role["permissions"])
        self.assertEqual(admins_role.position, role["position"])

    def test_role_post_201(self):
        """Tests creation of a role with a valid request."""
        url = reverse('bot:role-list', host='api')
        data = {
            "id": 1234567890,
            "name": "Role Creation Test",
            "permissions": 0b01010010101,
            "colour": 1,
            "position": 10,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

    def test_role_post_invalid_request_body(self):
        """Tests creation of a role with an invalid request body."""
        url = reverse('bot:role-list', host='api')
        data = {
            "name": "Role Creation Test",
            "permissions": 0b01010010101,
            "colour": 1,
            "position": 10,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, '{"id": ["This field is required."]}')

    def test_role_put_200(self):
        """Tests PUT role request with valid request body."""
        url = reverse('bot:role-detail', host='api', args=(self.admins_role.id,))
        data = {
            "id": 123454321,
            "name": "Role Put Alteration Test",
            "permissions": 255,
            "colour": 999,
            "position": 20,
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)

        admins_role = Role.objects.get(id=data["id"])
        self.assertEqual(admins_role.name, data["name"])
        self.assertEqual(admins_role.permissions, data["permissions"])
        self.assertEqual(admins_role.colour, data["colour"])
        self.assertEqual(admins_role.position, data["position"])

    def test_role_put_invalid_request_body(self):
        """Tests PUT role request with invalid request body."""
        url = reverse('bot:role-detail', host='api', args=(self.admins_role.id,))
        data = {
            "name": "Role Put Alteration Test",
            "permissions": 255,
            "colour": 999,
            "position": 20,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_role_patch_200(self):
        """Tests PATCH role request with valid request body."""
        url = reverse('bot:role-detail', host='api', args=(self.admins_role.id,))
        data = {
            "name": "Owners"
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)

        admins_role = Role.objects.get(id=self.admins_role.id)
        self.assertEqual(admins_role.name, data["name"])

    def test_role_delete_200(self):
        """Tests DELETE requests for existing role."""
        url = reverse('bot:role-detail', host='api', args=(self.admins_role.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_role_detail_404_all_methods(self):
        """Tests detail view with non-existing ID."""
        url = reverse('bot:role-detail', host='api', args=(20190815,))

        for method in ('get', 'put', 'patch', 'delete'):
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, 404)
            self.assertJSONEqual(response.content, '{"detail": "Not found."}')
