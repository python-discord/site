# The "timeline" app

The [timeline page](https://www.pythondiscord.com/timeline/) on our website is
powered by this Django application.

## The entries

Timeline entries are written in markdown files with YAML frontmatter under the
`entries` directory.

Each file represents a timeline entry. The file names have the format
`<date>_<name>.md`, where:
- `date` is in `YYYY-MM-DD` for easy sorting of files in directory listings,
  also used for sorting of the entries displayed on the timeline page.
- `name` is an arbitrary slug in `kebab-case`, used for linking to individual
  timeline entries on the page, which will be set in the `id` attribute for each
  timeline item.

Each file contains:
- A YAML frontmatter, which defines some metadata shown next to each entry in
  the timeline, including:
  - `date`: User-facing date label.
  - `icon`: The CSS class used for the icon, e.g. "fa fa-snowflake". Set to
    `pydis` to use the pydis logo image.
  - `icon_color`: The CSS class that sets the background color of the icon, e.g.
    "pastel-red". List of available colors can be found in [the CSS
    file](../../static/css/timeline/timeline.css). This can be omitted if the
    pydis logo is used.
- Markdown content.


## Directory structure

The app has a single view in `views.py` that renders the template using the list
of parsed entries from `apps.py`, which reads the markdown files on startup.
This is a standard Django view, mounted in `urls.py` as usual.

The `tests` directory validates that the page renders successfully as expected.
If you made changes to the app and are looking for guidance on adding new tests,
the [Django tutorial introducing automated
testing](https://docs.djangoproject.com/en/dev/intro/tutorial05/) is a good
place to start.

This application does not use the database and as such does not have models nor
migrations.
