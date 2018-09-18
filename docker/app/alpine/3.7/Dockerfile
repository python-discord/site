FROM python:3.7-alpine

ARG EXTRAS=deploy

RUN apk add \
        curl \
        gcc \
        musl-dev \
        postgresql-dev

WORKDIR /app
COPY setup.py /app/setup.py
RUN python3 -m pip install .[$EXTRAS]
COPY . .

RUN apk del \
        gcc

HEALTHCHECK CMD curl -I localhost:4000 || exit 1
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
