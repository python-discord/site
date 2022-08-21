FROM ghcr.io/chrislovering/python-poetry-base:3.10-slim

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Copy the project files into working directory
WORKDIR /app

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

# Set Git SHA environment variable
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Copy the source code in last to optimize rebuilding the image
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
    poetry run python manage.py collectstatic --noinput --clear

# Build static files if we are doing a static build
ARG STATIC_BUILD=false
RUN if [ $STATIC_BUILD = "TRUE" ] ; \
  then SECRET_KEY=dummy_value poetry run python manage.py distill-local build --traceback --force ; \
fi

# Run web server through custom manager
ENTRYPOINT ["poetry", "run", "python", "manage.py"]
CMD ["run"]
