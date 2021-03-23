---
title: How to Write a Article
short_description: Learn how to write a article for this website
icon_class: fas
icon: fa-info
---

When you are interested about how to write articles for this site (like this), then you can learn about it here.
PyDis use Markdown (GitHub Markdown) files for articles.

## Getting Started
Before you can get started with writing a article, you need idea.
Best way to find out is your idea good is to discuss about it in #dev-contrib channel. There can other peoples give their opinion about your idea. Even better, open issue in site repository first, then PyDis staff can see it and approve/decline this idea.
It's good idea to wait for staff decision before starting to write guide to avoid case when you write a long long article, but then this don't get approved.

To start with contributing, you should read [how to contribute to site](https://pythondiscord.com/pages/contributing/site/).
You should also read our [Git workflow](https://pythondiscord.com/pages/contributing/working-with-git/), because you need to push your guide to GitHub.

## Creating a File
All articles is located at `site` repository, in `pydis_site/apps/content/resources/content`. Under this is root level articles (.md files) and categories (directories). Learn more about categories in [categories section](#categories).

When you are writing guides, then these are located under `guides` category.

At this point, you will need your article name for filename. Replace all your article name spaces with `-` and make all lowercase. Save this as `.md` (Markdown) file. This name (without Markdown extension) is path of article in URL.

## Markdown Metadata
Article files have some required metadata, like title, description, relevant pages. Metadata is first thing in file, YAML-like key-value pairs:

```md
---
title: My Article
short_description: This is my short description.
relevant_links: url1,url2,url3
relevant_link_values: Text for url1,Text for url2,Text for url3
---

Here comes content of article...
```

You can read more about Markdown metadata [here](https://github.com/trentm/python-markdown2/wiki/metadata).

### Fields
- **Name:** Easily-readable name for your article.
- **Short Description:** Small, 1-2 line description that describe what your article explain.
- **Relevant Links and Values:** URLs and values is under different fields, separated with comma.
- **Icon class:** `icon_class` field have one of the favicons classes. Default is `fab`.
- **Icon:** `icon` field have favicon name. Default `fa-python`.

## Content
For content, mostly you can use standard markdown, but there is a few addition that is available.

### IDs for quick jumps
System automatically assign IDs to headers, so like this header will get ID `ids-for-quick-jumps`.

### Tables
Tables like in GitHub is supported too:

| This is header | This is too header |
| -------------- | ------------------ |
| My item        | My item too        |

### Codeblocks
Also this system supports codeblocks and provides syntax highlighting with `highlight.js`.
To activate syntax highlight, just put language directly after starting backticks.

```py
import os

path = os.path.join("foo", "bar")
```

## Categories
To have some systematic sorting of guides, site support guides categories. Currently this system support only 1 level of categories. Categories live at `site` repo in `pydis_site/apps/content/resources/content` subdirectories. Directory name is path of category in URL. Inside category directory, there is 1 file required: `_info.yml`. This file need 2 key-value pairs defined:

```yml
name: Category name
description: Category description
```

Then all Markdown files in this folder will be under this category.
