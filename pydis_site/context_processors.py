from django.template import RequestContext

from pydis_site.utils.resources import get_git_sha


def git_sha_processor(_: RequestContext) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': get_git_sha()}
