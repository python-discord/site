docker build -t build_uwsgi -f docker/app/build-wiki.Dockerfile .
CONTAINER=$(docker run -itd build_uwsgi /bin/bash)
docker cp "$CONTAINER:/wheels" docker/app
docker stop "$CONTAINER"
