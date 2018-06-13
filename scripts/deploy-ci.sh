#!/bin/bash

# Build and deploy on master branch
if [[ $CI_COMMIT_REF_SLUG == 'master' ]]; then
    echo "Connecting to docker hub"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    changed_lines=$(git diff HEAD~1 HEAD docker/base.Dockerfile | wc -l)

    if [ $changed_lines != '0' ]; then
      echo "base.Dockerfile was changed"

      echo "Building CI container"
      docker build -t pythondiscord/django-site-ci:latest -f docker/base.Dockerfile .

      echo "Pushing image to Docker Hub"
      docker push pythondiscord/django-site-ci:latest
    else
      echo "base.Dockerfile was not changed, not building"
    fi
else
    echo "Skipping CI Docker build"
fi
