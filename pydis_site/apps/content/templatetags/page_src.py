from django import template
from django.conf import settings


register = template.Library()


@register.filter()
def page_src_url(request_path: str) -> str:
    """
    Return the corresponding GitHub source URL for the current content article.

    request_path is the relative path of an article, as returned by `request.path` in templates.

    For example: /pages/rules/ would return:
    https://github.com/python-discord/site/tree/main/pydis_site/apps/content/resources/rules.md
    """
    src_url = request_path.replace("/pages/", settings.CONTENT_SRC_URL)
    src_url = src_url[:-1] + ".md"
    return src_url
