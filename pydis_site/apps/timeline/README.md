# The "timeline" app

The [timeline page](https://www.pythondiscord.com/timeline/) on our website is
powered by this Django application.

## The entries

Timeline entries are written in markdown files with YAML frontmatter under the
`entries` directory.

Each file represents a timeline entry. The files are named with the format
`<date>_<name>.md`:
- `date`: The date is in the `YYYY-MM-DD` format, intended for easy sorting in
  editor/shell command directory listings. It's also used to sort the entries
  before rendering the timeline page.
- `name`: The name component is an arbitrary slug in **kebab-case**. This is used
  for linking to individual timeline entries on the page, and will be set in
  the `id` attribute.

Each file contains:
- YAML frontmatter. This defines some metadata shown next to each entry in
  the timeline, including:
  - Date: User-facing date label.
  - Icon: The CSS class to be used for the icon. Set to `pydis` to use the
    pydis logo image.
  - Icon color: The CSS class that sets the background color of the icon. Leave
    empty if the pydis logo is used.
- Markdown content.


## Directory structure

The app has a single view in `views.py` that takes care of reading the `.md`
files in the `entires` directory. This is a standard Django view, mounted in
`urls.py` as usual.

The `tests` directory validates that our redirects and helper functions work as
expected. If you made changes to the app and are looking for guidance on adding
new tests, the [Django tutorial introducing automated
testing](https://docs.djangoproject.com/en/dev/intro/tutorial05/) is a good
place to start.

This application does not use the database and as such does not have models nor
migrations.
