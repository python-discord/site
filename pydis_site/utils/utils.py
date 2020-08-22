import git

# Git SHA
repo = git.Repo(search_parent_directories=True)
GIT_SHA = repo.head.object.hexsha


def get_git_sha() -> str:
    """Get the Git SHA for this repo."""
    return GIT_SHA
