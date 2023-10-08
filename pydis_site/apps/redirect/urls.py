import dataclasses
import re

import yaml
from django import conf
from django.urls import URLPattern, path

from pydis_site.apps.redirect.views import CustomRedirectView

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
    """Return a pattern using the Redirects app."""
    return [path(
        data.original_path,
        CustomRedirectView.as_view(
            pattern_name=data.redirect_route,
            static_args=tuple(data.redirect_arguments),
            prefix_redirect=data.prefix_redirect
        ),
        name=name
    )]


urlpatterns = []
for _name, _data in yaml.safe_load(conf.settings.REDIRECTIONS_PATH.read_text()).items():
    urlpatterns.extend(map_redirect(_name, Redirect(**_data)))
