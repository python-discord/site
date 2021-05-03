import yaml
from django.conf import settings
from django.urls import path

from pydis_site.apps.redirect.views import CustomRedirectView

app_name = "redirect"
urlpatterns = [
    path(
        data["original_path"],
        CustomRedirectView.as_view(
            pattern_name=data["redirect_route"],
            static_args=tuple(data.get("redirect_arguments", ())),
            prefix_redirect=data.get("prefix_redirect", False)
        ),
        name=name
    )
    for name, data in yaml.safe_load(settings.REDIRECTIONS_PATH.read_text()).items()
]
