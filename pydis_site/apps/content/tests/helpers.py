import tempfile

from pyfakefs.fake_filesystem_unittest import TestCase

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

    Structure:
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
        self.setUpPyfakefs()

        self.fs.create_file("_info.yml", contents=CATEGORY_INFO)
        self.fs.create_file("root.md", contents=MARKDOWN_WITH_METADATA)
        self.fs.create_file("root_without_metadata.md", contents=MARKDOWN_WITHOUT_METADATA)
        self.fs.create_file("not_a_page.md/_info.yml", contents=CATEGORY_INFO)
        self.fs.create_file("category/_info.yml", contents=CATEGORY_INFO)
        self.fs.create_file("category/with_metadata.md", contents=MARKDOWN_WITH_METADATA)
        self.fs.create_file("category/subcategory/_info.yml", contents=CATEGORY_INFO)
        self.fs.create_file(
            "category/subcategory/with_metadata.md", contents=MARKDOWN_WITH_METADATA
        )
        self.fs.create_file(
            "category/subcategory/without_metadata.md", contents=MARKDOWN_WITHOUT_METADATA
        )

        # There is always a `tmp` directory in the filesystem, so make it a category
        # for testing purposes.
        # See: https://jmcgeheeiv.github.io/pyfakefs/release/usage.html#os-temporary-directories
        self.populate_tempdir('tmp')

        # Some systems do not use `/tmp` as their temporary directory, such as macOS,
        # which means that we will have an additional folder in the root directory
        # to deal with. To prevent this from causing any errors during tests, we
        # also populate the platform-specific temp directory. It is populated in
        # addition to `/tmp`, as some files are tested in `/tmp`.
        _, tmpname, *_rest = tempfile.gettempdir().split('/')
        if tmpname != 'tmp':
            self.populate_tempdir(tmpname)

        self.os_tmpname = tmpname

    def populate_tempdir(self, name: str) -> None:
        """Populate contents of the OS temp directory."""
        self.fs.create_file(f"{name}/_info.yml", contents=CATEGORY_INFO)
        self.fs.create_file(f"{name}.md", contents=MARKDOWN_WITH_METADATA)
        self.fs.create_file(f"{name}/category/_info.yml", contents=CATEGORY_INFO)
        self.fs.create_dir(f"{name}/category/subcategory_without_info")
