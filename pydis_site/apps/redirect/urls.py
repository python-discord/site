import dataclasses
import re

import yaml
from django import conf
from django.urls import URLPattern, path
from django_distill import distill_path

from pydis_site import settings
from pydis_site.apps.content import urls as pages_urls
from pydis_site.apps.redirect.views import CustomRedirectView
from pydis_site.apps.resources import urls as resources_urls

app_name = "redirect"


__PARAMETER_REGEX = re.compile(r"<\w+:\w+>")
REDIRECT_TEMPLATE = "<meta http-equiv=\"refresh\" content=\"0; URL={url}\"/>"


@dataclasses.dataclass(frozen=True)
class Redirect:
    """Metadata about a redirect route."""

    original_path: str
    redirect_route: str
    redirect_arguments: tuple[str] = tuple()

    prefix_redirect: bool = False


def map_redirect(name: str, data: Redirect) -> list[URLPattern]:
    """Return a pattern using the Redirects app, or a static HTML redirect for static builds."""
    if not settings.env("STATIC_BUILD"):
        # Normal dynamic redirect
        return [path(
            data.original_path,
            CustomRedirectView.as_view(
                pattern_name=data.redirect_route,
                static_args=tuple(data.redirect_arguments),
                prefix_redirect=data.prefix_redirect
            ),
            name=name
        )]

    # Create static HTML redirects for static builds
    new_app_name = data.redirect_route.split(":")[0]

    if __PARAMETER_REGEX.search(data.original_path):
        # Redirects for paths which accept parameters
        # We generate an HTML redirect file for all possible entries
        paths = []

        class RedirectFunc:
            def __init__(self, new_url: str, _name: str):
                self.result = REDIRECT_TEMPLATE.format(url=new_url)
                self.__qualname__ = _name

            def __call__(self, *args, **kwargs):
                return self.result

        if new_app_name == resources_urls.app_name:
            items = resources_urls.get_all_resources()
        elif new_app_name == pages_urls.app_name:
            items = pages_urls.get_all_pages()
        else:
            raise ValueError(f"Unknown app in redirect: {new_app_name}")

        for item in items:
            entry = list(item.values())[0]

            # Replace dynamic redirect with concrete path
            concrete_path = __PARAMETER_REGEX.sub(entry, data.original_path)
            new_redirect = f"/{new_app_name}/{entry}"
            pattern_name = f"{name}_{entry}"

            paths.append(distill_path(
                concrete_path,
                RedirectFunc(new_redirect, pattern_name),
                name=pattern_name
            ))

        return paths

    else:
        redirect_path_name = "pages" if new_app_name == "content" else new_app_name
        if len(data.redirect_arguments) > 0:
            redirect_arg = data.redirect_arguments[0]
        else:
            redirect_arg = "resources/"
        new_redirect = f"/{redirect_path_name}/{redirect_arg}"

        if new_redirect == "/resources/resources/":
            new_redirect = "/resources/"

        return [distill_path(
            data.original_path,
            lambda *args: REDIRECT_TEMPLATE.format(url=new_redirect),
            name=name,
        )]


urlpatterns = []
for _name, _data in yaml.safe_load(conf.settings.REDIRECTIONS_PATH.read_text()).items():
    urlpatterns.extend(map_redirect(_name, Redirect(**_data)))
