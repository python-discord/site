# coding=utf-8
from docutils import nodes
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst.states import Inliner
from flask import url_for
from jinja2 import escape


def icon_role(_role: str, rawtext: str, text: str, lineno: int, inliner: Inliner,
              options: dict = None, _content: dict = None):
    if options is None:
        options = {}

    set_classes(options)

    if "/" in text:
        parts = [escape(x) for x in text.split("/")]
    else:
        msg = inliner.reporter.error("Icon specification must be in the form <type>/<name>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]

    if len(parts) != 2:
        msg = inliner.reporter.error("Icon specification must be in the form <type>/<name>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]
    else:
        if parts[0] == "light":
            weight = "fal"
        elif parts[0] == "regular":
            weight = "far"
        elif parts[0] == "solid":
            weight = "fas"
        elif parts[0] == "branding":
            weight = "fab"
        else:
            msg = inliner.reporter.error("Icon type must be one of light, regular, solid or branding", line=lineno)
            prb = inliner.problematic(text, rawtext, msg)

            return [prb], [msg]

        html = f"""<i class="uk-icon {weight} fa-{parts[1]}"></i>"""

        node = nodes.raw(html, html, format="html", **options)
        return [node], []


def url_for_role(_role: str, rawtext: str, text: str, lineno: int, inliner: Inliner,
                 options: dict = None, _content: dict = None):
    if options is None:
        options = {}

    set_classes(options)

    if "/" in text:
        parts = [escape(x) for x in text.split("/")]
    else:
        msg = inliner.reporter.error("URL specification must be in the form <page.name>/<text>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]

    if len(parts) != 2:
        msg = inliner.reporter.error("URL specification must be in the form <page.name>/<text>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]
    else:
        try:
            url = url_for(parts[0])
            name = parts[1]

            html = f"""<a href="{url}">{name}</a>"""

            node = nodes.raw(html, html, format="html", **options)
            return [node], []
        except Exception as e:
            msg = inliner.reporter.error(str(e), line=lineno)
            prb = inliner.problematic(text, rawtext, msg)

            return [prb], [msg]


def page_role(_role: str, rawtext: str, text: str, lineno: int, inliner: Inliner,
                 options: dict = None, _content: dict = None):
    if options is None:
        options = {}

    set_classes(options)

    if "/" in text:
        parts = [escape(x) for x in text.split("/")]
    else:
        msg = inliner.reporter.error("Page specification must be in the form <page_slug>/<text>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]

    if len(parts) != 2:
        msg = inliner.reporter.error("Page specification must be in the form <page_slug>/<text>", line=lineno)
        prb = inliner.problematic(text, rawtext, msg)

        return [prb], [msg]
    else:
        try:
            url = url_for("wiki.page", page=parts[0])
            name = parts[1]

            html = f"""<a href="{url}">{name}</a>"""

            node = nodes.raw(html, html, format="html", **options)
            return [node], []
        except Exception as e:
            msg = inliner.reporter.error(str(e), line=lineno)
            prb = inliner.problematic(text, rawtext, msg)

            return [prb], [msg]
