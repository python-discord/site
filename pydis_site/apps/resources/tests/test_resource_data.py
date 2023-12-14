import yaml
from django.test import TestCase

from pydis_site.apps.resources.views import RESOURCES_PATH


class TestResourceData(TestCase):
    """Test data validity of resources."""

    def test_no_duplicate_links(self):
        """Test that there are no duplicate links in each resource."""
        for path in RESOURCES_PATH.rglob('*.yaml'):
            with self.subTest(resource=path.stem):
                content = yaml.safe_load(path.read_text())
                url_links = tuple(item['url'] for item in content.get('urls', ()))
                if 'title_url' in content:
                    all_links = url_links + (content['title_url'],)
                else:
                    all_links = url_links

                self.assertCountEqual(
                    all_links,
                    set(all_links),
                    msg="One or more links are duplicated on the resource",
                )
