from django import template

register = template.Library()


@register.filter()
def page_github(current_uri: str):
    return current_uri.replace(
        "https://pythondiscord.com/pages/",
        "https://github.com/python-discord/site/tree/main/pydis_site/apps/content/resources"
    )
