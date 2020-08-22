from django.template import RequestContext

from pydis_site.constants import GIT_SHA


def git_sha_processor(_: RequestContext) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': GIT_SHA}
