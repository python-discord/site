# The "content" app

This application serves static, Markdown-based content. Django-wise there is
relatively little code in there; most of it is concerned with serving our
content.


## Contributing pages

The Markdown files hosting our content can be found in the
[`resources/`](./resources) directory. The process of contributing to pages is
covered extensively in our online guide which you can find
[here](https://www.pythondiscord.com/pages/guides/pydis-guides/how-to-contribute-a-page/).
Alternatively, read it directly at
[`resources/guides/pydis-guides/how-to-contribute-a-page.md`](./resources/guides/pydis-guides/how-to-contribute-a-page.md).


## Directory structure

Let's look at the structure in here:

- `resources` contains the static Markdown files that make up our site's
  [pages](https://www.pythondiscord.com/pages/)

- `migrations` contains standard Django migrations. As the `content` app
  contains purely static Markdown files, no migrations are present here.

- `tests` contains unit tests for verifying that the app works properly.

- `views` contains Django views which generating and serve the pages from the
  input Markdown.

As for the modules, apart from the standard Django modules in here, the
`utils.py` module contains utility functions for discovering Markdown files to
serve.
