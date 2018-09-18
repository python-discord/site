FROM python:3.7-alpine

ARG EXTRAS=deploy

RUN apk add \
        automake \
        cmake \
        gcc \
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
        gcc

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
