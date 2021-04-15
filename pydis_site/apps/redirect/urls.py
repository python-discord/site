from django.conf import settings
from django.urls import path

from pydis_site.apps.redirect.views import CustomRedirectView

app_name = "redirect"
urlpatterns = [
    path(
        original,
        CustomRedirectView.as_view(
            pattern_name=redirect_route,
            static_args=params
        ),
        name=name
    )
    for original, (redirect_route, name, params) in settings.REDIRECTIONS.items()
]
