from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

app_name = "redirect"
urlpatterns = [
    path(original, RedirectView.as_view(pattern_name=redirect_route), name=name)
    for original, (redirect_route, name, _) in settings.REDIRECTIONS.items()
]
