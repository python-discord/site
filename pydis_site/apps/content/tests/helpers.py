import atexit
import shutil
import tempfile
from pathlib import Path

from django.test import TestCase


BASE_PATH = Path(tempfile.mkdtemp(prefix='pydis-site-content-app-tests-'))
atexit.register(shutil.rmtree, BASE_PATH, ignore_errors=True)


# Valid markdown content with YAML metadata
MARKDOWN_WITH_METADATA = """
---
title: TestTitle
description: TestDescription
relevant_links:
    Python Discord: https://pythondiscord.com
    Discord: https://discord.com
toc: 0
---
# This is a header.
"""

MARKDOWN_WITHOUT_METADATA = """#This is a header."""

# Valid YAML in a _info.yml file
CATEGORY_INFO = """
title: Category Name
description: Description
"""

# The HTML generated from the above markdown data
PARSED_HTML = (
    '<h1 id="this-is-a-header">This is a header.'
    '<a class="headerlink" href="#this-is-a-header" title="Permanent link">&para;</a></h1>'
)

# The YAML metadata parsed from the above markdown data
PARSED_METADATA = {
    "title": "TestTitle", "description": "TestDescription",
    "relevant_links": {
        "Python Discord": "https://pythondiscord.com",
        "Discord": "https://discord.com"
    },
    "toc": 0
}

# The YAML data parsed from the above _info.yml file
PARSED_CATEGORY_INFO = {"title": "Category Name", "description": "Description"}


class MockPagesTestCase(TestCase):
    """
    TestCase with a fake filesystem for testing.

    Structure (relative to BASE_PATH):
    ├── _info.yml
    ├── root.md
    ├── root_without_metadata.md
    ├── not_a_page.md
    ├── tmp.md
    ├── tmp
    |   ├── _info.yml
    |   └── category
    |       ├── _info.yml
    |       └── subcategory_without_info
    └── category
        ├── _info.yml
        ├── with_metadata.md
        └── subcategory
            ├── with_metadata.md
            └── without_metadata.md
    """

    def setUp(self):
        """Create the fake filesystem."""
        Path(f"{BASE_PATH}/_info.yml").write_text(CATEGORY_INFO)
        Path(f"{BASE_PATH}/root.md").write_text(MARKDOWN_WITH_METADATA)
        Path(f"{BASE_PATH}/root_without_metadata.md").write_text(MARKDOWN_WITHOUT_METADATA)
        Path(f"{BASE_PATH}/not_a_page.md").mkdir(exist_ok=True)
        Path(f"{BASE_PATH}/not_a_page.md/_info.yml").write_text(CATEGORY_INFO)
        Path(f"{BASE_PATH}/category").mkdir(exist_ok=True)
        Path(f"{BASE_PATH}/category/_info.yml").write_text(CATEGORY_INFO)
        Path(f"{BASE_PATH}/category/with_metadata.md").write_text(MARKDOWN_WITH_METADATA)
        Path(f"{BASE_PATH}/category/subcategory").mkdir(exist_ok=True)
        Path(f"{BASE_PATH}/category/subcategory/_info.yml").write_text(CATEGORY_INFO)
        Path(
            f"{BASE_PATH}/category/subcategory/with_metadata.md"
        ).write_text(MARKDOWN_WITH_METADATA)
        Path(
            f"{BASE_PATH}/category/subcategory/without_metadata.md"
        ).write_text(MARKDOWN_WITHOUT_METADATA)

        temp = f"{BASE_PATH}/tmp"  # noqa: S108
        Path(f"{temp}").mkdir(exist_ok=True)
        Path(f"{temp}/_info.yml").write_text(CATEGORY_INFO)
        Path(f"{temp}.md").write_text(MARKDOWN_WITH_METADATA)
        Path(f"{temp}/category").mkdir(exist_ok=True)
        Path(f"{temp}/category/_info.yml").write_text(CATEGORY_INFO)
        Path(f"{temp}/category/subcategory_without_info").mkdir(exist_ok=True)
