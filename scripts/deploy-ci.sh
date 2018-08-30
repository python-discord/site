#!/bin/bash

# Build and deploy on master branch
echo "Connecting to docker hub"
echo "$GITLAB_DOCKER_PASSWORD" | docker login --username "$GITLAB_DOCKER_USERNAME" --password-stdin registry.gitlab.com

changed_lines=$(git diff HEAD~1 HEAD docker/base.Dockerfile | wc -l)

if [ $changed_lines != '0' ]; then
  echo "base.Dockerfile was changed"

  echo "Building CI container"
  docker build -t registry.gitlab.com/python-discord/projects/site/django-base:latest -f docker/base.Dockerfile .

  echo "Pushing image to GitLab registry"
  docker push registry.gitlab.com/python-discord/projects/site/django-base:latest
else
  echo "base.Dockerfile was not changed, not building"
fi
