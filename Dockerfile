# When updating the Python version here, please make sure to also
# update the contributor guide, which can be found at
#   pydis_site/apps/content/resources/guides/pydis-guides/contributing/site.md
# Thank you!
ARG python_version=3.13-slim

FROM python:$python_version AS builder
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /bin/

ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

# Install project dependencies with build tools available
WORKDIR /build

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-dev

FROM python:$python_version

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Set Git SHA environment variable
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Install dependencies from build cache
# .venv not put in /app so that it doesn't conflict with the dev
# volume we use to avoid rebuilding image every code change locally
COPY --from=builder /build /build
COPY --from=builder /bin/uv /bin/uv
ENV PATH="/build/.venv/bin:$PATH"

# Copy the source code in last to optimize rebuilding the image
WORKDIR /app
COPY . .

# Set dummy variables so collectstatic can load settings.py
RUN \
    # Set BUILDING_DOCKER to anything but undefined so settings.py
    # does not insert django_prometheus into the list of installed apps.
    # This prevents django_prometheus from attempting to connect to the database
    # when the collectstatic task is ran.
    BUILDING_DOCKER=yes \
    SECRET_KEY=dummy_value \
    DATABASE_URL=postgres://localhost \
    METRICITY_DB_URL=postgres://localhost \
    uv run python manage.py collectstatic --noinput --clear

# Build static files if we are doing a static build
ARG STATIC_BUILD=false
RUN if [ $STATIC_BUILD = "TRUE" ] ; \
  then SECRET_KEY=dummy_value uv run python manage.py distill-local build --traceback --force ; \
fi

CMD ["gunicorn", "--preload", "-b", "0.0.0.0:8000", \
     "pydis_site.wsgi:application", "-w", "2", "--statsd-host", \
     "graphite.default.svc.cluster.local:8125", "--statsd-prefix", "site", \
     "--config", "file:gunicorn.conf.py"]
