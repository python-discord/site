import git
from django.template import RequestContext

REPO = git.Repo(search_parent_directories=True)
SHA = REPO.head.object.hexsha


def git_sha_processor(_: RequestContext) -> dict:
    """Expose the git SHA for this repo to all views."""
    return {'git_sha': SHA}
