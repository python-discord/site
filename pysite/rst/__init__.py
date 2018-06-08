import re

from docutils.core import publish_parts
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.roles import register_canonical_role

from pysite.rst.directives import ButtonDirective
from pysite.rst.roles import fira_code_role, icon_role, page_role, url_for_role

RST_TEMPLATE = """.. contents::

{0}"""

CONTENTS_REGEX = re.compile(r"""<div class=\"contents topic\" id=\"contents\">(.*?)</div>""", re.DOTALL)
HREF_REGEX = re.compile(r"""<a class=\"reference internal\" href=\"(.*?)\".*?>(.*?)</a>""")

TABLE_FRAGMENT = """<table class="uk-table uk-table-divider table-bordered uk-table-striped">"""


def render(rst: str, link_headers=True):
    if link_headers:
        rst = RST_TEMPLATE.format(rst)

    html = publish_parts(
        source=rst, writer_name="html5", settings_overrides={
            "halt_level": 2, "syntax_highlight": "short", "initial_header_level": 3
        }
    )["html_body"]

    data = {
        "html": html,
        "headers": []
    }

    if link_headers:
        match = CONTENTS_REGEX.search(html)  # Find the contents HTML

        if match:
            data["html"] = html.replace(match.group(0), "")  # Remove the contents from the document HTML
            depth = 0
            headers = []
            current_header = {}

            group = match.group(1)

            # Sanitize the output so we can more easily parse it
            group = group.replace("<li>", "<li>\n")
            group = group.replace("</li>", "\n</li>")
            group = group.replace("<p>", "<p>\n")
            group = group.replace("</p>", "\n</p>")

            for line in group.split("\n"):
                line = line.strip()  # Remove excess whitespace

                if not line:  # Nothing to process
                    continue

                if line.startswith("<li>") and depth <= 2:
                    #  We've found a header, or the start of a header group
                    depth += 1
                elif line.startswith("</li>") and depth >= 0:
                    # That's the end of a header or header group

                    if depth == 1:
                        # We just dealt with an entire header group, so store it
                        headers.append(current_header.copy())  # Store a copy, since we're clearing the dict
                        current_header.clear()

                    depth -= 1
                elif line.startswith("<a") and depth <= 2:
                    # We've found an actual URL
                    match = HREF_REGEX.match(line)  # Parse the line for the ID and header title

                    if depth == 1:  # Top-level header, so just store it in the current header
                        current_header["id"] = match.group(1)

                        title = match.group(2)

                        if title.startswith("<i"):  # We've found an icon, which needs to have a space after it
                            title = title.replace("</i> ", "</i> &nbsp;")

                        current_header["title"] = title
                    else:  # Second-level (or deeper) header, should be stored in a list of sub-headers
                        sub_headers = current_header.get("sub_headers", [])
                        title = match.group(2)

                        if title.startswith("<i"):  # We've found an icon, which needs to have a space after it
                            title = title.replace("</i> ", "</i> &nbsp;")

                        sub_headers.append({
                            "id": match.group(1),
                            "title": title
                        })
                        current_header["sub_headers"] = sub_headers

            data["headers"] = headers

    data["html"] = data["html"].replace("<table>", TABLE_FRAGMENT)  # Style the tables properly

    return data


register_canonical_role("fira_code", fira_code_role)
register_canonical_role("icon", icon_role)
register_canonical_role("page", page_role)
register_canonical_role("url_for", url_for_role)

register_directive("button", ButtonDirective)
