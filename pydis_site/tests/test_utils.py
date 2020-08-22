from django.test import TestCase

from pydis_site.utils import get_git_sha
from pydis_site.utils.utils import GIT_SHA


class UtilsTests(TestCase):

    def test_git_sha(self):
        """Test that the get_git_sha returns the correct SHA."""
        self.assertEqual(get_git_sha(), GIT_SHA)
