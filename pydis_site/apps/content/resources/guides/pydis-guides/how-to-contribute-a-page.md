---
title: How to Contribute a Page
description: Learn how to write and publish a page to this website.
icon: fas fa-info
relevant_links:
    Contributing to Site: https://pythondiscord.com/pages/contributing/site/
    Using Git: https://pythondiscord.com/pages/contributing/working-with-git/
---

Pages, which include guides, articles, and other static content, are stored in markdown files in the `site` repository on Github.
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

#### Page Categories
Nested folders represent page categories on the website. Each folder under the root folder must include a `_info.yml` file with the following:

```yml
title: Category name
description: Category description
icon: fas fa-folder # Optional
```

All the markdown files in this folder will then be under this category.

#### Having the Category also be a Page
In order to make categories a page, place a page inside the category folder **with the same name as the category folder**.

```plaintext
guides
├── contributing
│   ├── _info.yml
│   ├── contributing.md
│   └── bot.md
└── _info.yml
```

In the above example, `www.pythondiscord.com/guides/` will list `Contributing` as a category entry with information from `contributing/_info.yml`.

However, `www.pythondiscord.com/guides/contributing` will render `contributing.md` rather than show the category contents, so *it is the article's responsibility to link to any subpages under the article*.

Therefore, `www.pythondiscord.com/guides/contributing/bot` will then render `bot.md`, with backlinks to `contributing.md`.

## Writing the Page
Files representing pages are in `.md` (Markdown) format, with all-lowercase filenames and spaces replaced with `-` characters.

Each page must include required metadata, and optionally additional metadata to modify the appearance of the page.
The metadata is written in YAML, and should be enclosed in triple dashes `---` *at the top of the markdown file*.

**Example:**
```yaml
---
title: How to Contribute a Page
description: Learn how to write and publish a page to this website.
icon: fas fa-info
relevant_links:
    Contributing to Site: https://pythondiscord.com/pages/contributing/site/
    Using Git: https://pythondiscord.com/pages/contributing/working-with-git/
---

Pages, which include guides, articles, and other static content,...
```

### Required Fields
- **title:** Easily-readable title for your article.
- **description:** Short, 1-2 line description of the page's content.

### Optional Fields
- **icon:** Icon for the category entry for the page. Default: `fab fa-python` <i class="fab fa-python is-black" aria-hidden="true"></i>
- **relevant_links:** A YAML dictionary containing `text:link` pairs. See the example above.

## Extended Markdown

Apart from standard Markdown, certain additions are available:

### Abbreviations
HTML `<abbr>` tags can be used in markdown using this format:

**Markdown:**
```nohighlight
This website is HTML generated from YAML and Markdown.

*[HTML]: Hyper Text Markup Language
*[YAML]: YAML Ain't Markup Language
```

**Output:**

This website is <abbr title="Hyper Text Markup Language">HTML</abbr>
generated from <abbr title="YAML Ain't Markup Language">YAML</abbr> and Markdown.

---

### Footnotes
**Markdown:**
```nohighlight
This footnote[^1] links to the bottom[^custom_label] of the page[^3].

[^1]: Footnote labels start with a caret `^`.
[^3]: The footnote link is numbered based on the order of the labels.
[^custom label]: Footnote labels can contain any text within square brackets.
```

**Output:**

This footnote[^1] links to the bottom[^custom label] of the page[^3].

[^1]: Footnote labels start with a caret `^`.
[^3]: The footnote link is numbered based on the order of the labels.
[^custom label]: Footnote labels can contain any text within square brackets.

---

### Tables

**Markdown:**
```nohighlight
| This is header | This is another header |
| -------------- | ---------------------- |
| An item        | Another item           |
```

**Output:**

| This is header | This is another header |
| -------------- | ---------------------- |
| An item        | Another item           |

---

### Codeblock Syntax Highlighting
Syntax highlighting is provided by `highlight.js`.
To activate syntax highlighting, put the language directly after the starting backticks.

**Markdown:**
````nohighlight
```python
import os

path = os.path.join("foo", "bar")
```
````

**Output:**
```python
import os

path = os.path.join("foo", "bar")
```

---

### HTML Attributes
To add HTML attributes to certain lines/paragraphs, [see this page](https://python-markdown.github.io/extensions/attr_list/#the-list) for the format and where to put it.

This can be useful for setting the image size when adding an image using markdown (see the [Image Captions](#image-captions) section for an example), or for adding bulma styles to certain elements (like the warning notification [here](/pages/guides/pydis-guides/contributing/sir-lancebot#setup-instructions)).  
**This should be used sparingly, as it reduces readability and simplicity of the article.**

---

### Image Captions
To add an image caption, place a sentence with italics *right below* the image link

**Markdown:**
```nohighlight
![Summer Code Jam 2020](/static/images/events/summer_code_jam_2020.png){: width="400" }
*Summmer Code Jam 2020 banner with event information.*
```

**Output:**

![Summer Code Jam 2020](/static/images/events/summer_code_jam_2020.png){: width="400"}
*Summer Code Jam 2020 banner with event information.*

> Note: To display a regular italicized line below an image, leave an empty line between the two.