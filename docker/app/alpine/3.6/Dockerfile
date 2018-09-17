FROM python:3.6-alpine

ARG EXTRAS=deploy

RUN apk add \
        autoconf \
        automake \
        cmake \
        gcc \
        git \
        libpq \
        musl-dev \
        postgresql-dev

COPY . /app
WORKDIR /app
RUN python3 -m pip install .[$EXTRAS]

RUN apk del \
        autoconf \
        automake \
        cmake \
        gcc \
        git

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
