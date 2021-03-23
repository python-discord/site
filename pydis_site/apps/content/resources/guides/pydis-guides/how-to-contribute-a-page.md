---
title: How to Contribute a Page
description: Learn how to write and publish a page to this website.
icon_class: fas
icon: fa-info
relevant_links:
    Contributing to Site: https://pythondiscord.com/pages/contributing/site/
    Using Git: https://pythondiscord.com/pages/contributing/working-with-git/
---

Pages, which include guides, articles and other static content are stored in markdown files in the `site` repository on Github.
If you are interested in writing or modifying pages seen here on the site, follow the steps below.

For further assistance and help with contributing pages, send a message to the `#dev-contrib` channel in the Discord server!

## Prerequisites
Before working on a new page, you have to [setup the site project locally](https://pythondiscord.com/pages/contributing/site/).
It is also a good idea to familiarize yourself with the [git workflow](https://pythondiscord.com/pages/contributing/working-with-git/), as it is part of the contribution workflow.

Additionally, please submit your proposed page or modification to a page as an [issue in the site repository](https://github.com/python-discord/site/issues), or discuss it in the `#dev-contrib` channel in the server.
As website changes require staff approval, discussing the page content beforehand helps with accelerating the contribution process, and avoids wasted work in the event the proposed page is not accepted.

## Creating the Page
All pages are located in the `site` repo, at the path `pydis_site/apps/content/resources/`. This is the root folder, which corresponds to the URL `www.pythondiscord.com/pages/`.
For example, the file `pydis_site/apps/content/resources/hello-world.md` will result in a page available at `www.pythondiscord.com/pages/hello-world`.

Nested folders represent page categories on the website. Each folder under the root folder must include a `_info.yml` file with the following:

```yml
name: Category name
description: Category description
```

All the markdown files in this folder will then be under this category.

## Writing the Page
Files representing pages are in `.md` (Markdown) format, with all-lowercase filenames and spaces replaced with `-` characters.

Each page must include required metadata, and optionally additional metadata to modify appearance of the page.
The metadata is written in YAML-like key-value pairs, and should be enclosed in triple dashes `---` *at the top of the markdown file*.

**Example:**
```yaml
---
title: How to Contribute a Page
description: Learn how to write and publish a page to this website.
icon_class: fas
icon: fa-info
relevant_links:
    Contributing to Site: https://pythondiscord.com/pages/contributing/site/
    Using Git: https://pythondiscord.com/pages/contributing/working-with-git/
---

Pages, which include guides, articles and other static content...
```

You can learn more about Markdown metadata [here](https://github.com/trentm/python-markdown2/wiki/metadata).

### Required Fields
- **title:** Easily-readable title for your article.
- **description:** Short, 1-2 line description that describes the page.

### Optional Fields
- **icon_class:** Favicon class for the category entry for the page. Default: `fab`
- **icon:** Favicon for the category entry for the page. Default: `fa-python` <i class="fab fa-python is-black" aria-hidden="true"></i>
- **relevant_links:** A YAML dictionary containing `text:link` pairs. See the example above.

## Extended Markdown

Apart from standard markdown, certain additions are available:

### Tables

| This is header | This is another header |
| -------------- | ---------------------- |
| An item        | Another item           |
| Big item       | Small item             |


### Codeblock Syntax Highlighting
Syntax highlighting is provided by `highlight.js`.
To activate syntax highlighting, put the language directly after the starting backticks.

```python
import os

path = os.path.join("foo", "bar")
```
