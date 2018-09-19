FROM python:3.6-alpine

ARG EXTRAS=deploy

# Build-time dependencies: To be removed later.
RUN apk add --virtual build \
        gcc \
        musl-dev

# Used by the healthcheck and shared library used by psycopg2.
RUN apk add --no-cache curl postgresql-dev

WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
# Remove dependencies used for building psycopg2.
RUN apk del --purge build

COPY . .

HEALTHCHECK CMD curl -I -f localhost:4000
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
