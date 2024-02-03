from django.conf import settings
from django.http import HttpRequest


def git_sha_processor(_: HttpRequest) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': settings.GIT_SHA}
