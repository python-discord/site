FROM bitnami/python:3.7-prod

# I have no idea what this does.
STOPSIGNAL SIGQUIT
ARG EXTRAS=deploy

ENV PIP_NO_CACHE_DIR=false \
    PIPENV_HIDE_EMOJIS=1 \
    PIPENV_NOSPIN=1

# Create a user.
RUN useradd --system --shell /bin/false --uid 1500 pysite

# Install prerequisites needed to complete the dependency installation.
RUN install_packages git uwsgi

# Copy the project files into the working directory.
WORKDIR /app
COPY . .

# Update setuptools by removing egg first, add other dependencies
RUN rm -r /opt/bitnami/python/lib/python3.*/site-packages/setuptools* && \
    pip install --no-cache-dir -U setuptools pipenv
RUN pipenv install --system --deploy

# Migrate, collect and start the app.
RUN chmod +x /app/docker/app/scripts/migrate.sh
ENTRYPOINT ["/app/docker/app/scripts/migrate.sh"]
CMD ["uwsgi", "--ini", "docker/app/uwsgi.ini"]
