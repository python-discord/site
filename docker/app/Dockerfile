FROM bitnami/python:3.7-prod

# I have no idea what this does.
STOPSIGNAL SIGQUIT
ARG EXTRAS=deploy

# Create a user.
RUN adduser \
    --disabled-login \
    --no-create-home \
    --uid 1500 \
    pysite

# Install prerequisites needed to complete the dependency installation.
RUN apt-get update -y \
    && \
        apt-get install --no-install-recommends -y \
                gcc \
                libc-dev \
                libpq-dev \
                git \
    && \
        apt-get clean \
    && \
        rm -rf /var/lib/apt/lists/*

# Set up the working directory.
WORKDIR /app
COPY Pipfile Pipfile.lock /app/

# Pip install the stuff we'll need.
RUN rm -r /opt/bitnami/python/lib/python3.*/site-packages/setuptools* && \
    pip install --no-cache-dir -U setuptools
RUN python3 -m pip install pipenv \
    && python3 -m pipenv install --system --deploy \
    && pip install uwsgi==2.0.18

# Copy everything into the docker environment.
COPY . .

# RUN SECRET_KEY=placeholder DATABASE_URL=sqlite:// python3 manage.py collectstatic --no-input --clear --verbosity 0

# Remove the prerequisites, dependency installation is now complete.
RUN apt-get purge -y \
            gcc \
            libc-dev \
            libpq-dev

# Migrate, collect and start the app.
RUN chmod +x /app/docker/app/scripts/migrate.sh
ENTRYPOINT ["/app/docker/app/scripts/migrate.sh"]
CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
