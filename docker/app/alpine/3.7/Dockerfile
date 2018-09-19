FROM python:3.7-alpine

ARG EXTRAS=deploy

# Build-time dependencies: To be removed later.
RUN apk add --virtual build \
        gcc \
        musl-dev \
        postgresql-dev

# Used by the healthcheck.
RUN apk add --no-cache curl

WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
# Remove dependencies used for building psycopg2.
RUN apk del --purge build

COPY . .

HEALTHCHECK CMD curl -I -f localhost:4000
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
