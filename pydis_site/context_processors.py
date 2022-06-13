from django.conf import settings
from django.template import RequestContext


def git_sha_processor(_: RequestContext) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': settings.GIT_SHA}
