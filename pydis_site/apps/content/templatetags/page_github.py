import requests
from django import template

register = template.Library()


@register.filter()
def page_github(current_uri: str) -> str:
    """
    Return the corresponding GitHub page for the current site page.

    Return a directory if the page is a directory on GitHub otherwise return the Markdown file
    """
    github_uri = current_uri.replace(
        "http://pythondiscord.local:8000/pages/",
        "https://github.com/python-discord/site/tree/main/pydis_site/apps/content/resources/"
    )
    github_uri = github_uri[:-1] if github_uri.endswith("/") else github_uri
    if requests.get(github_uri).status_code == 404:
        github_uri += ".md"
    return github_uri
