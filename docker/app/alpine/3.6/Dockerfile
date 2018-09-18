FROM python:3.6-alpine

ARG EXTRAS=deploy

RUN apk add \
        automake \
        cmake \
        gcc \
        git \
        libpq \
        musl-dev \
        postgresql-dev

WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apk del \
        automake \
        cmake \
        gcc \
        git

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
