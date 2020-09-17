import git

# Git SHA
repo = git.Repo(search_parent_directories=True)
GIT_SHA = repo.head.object.hexsha
