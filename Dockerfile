FROM python:3.7-alpine

RUN apk add python3-dev git libpq postgresql-dev gcc cmake autoconf automake musl-dev
RUN python3 -m pip install poetry

COPY . /app
WORKDIR /app

RUN python3 -m poetry config settings.virtualenvs.in-project true
RUN poetry install --no-dev
RUN apk del git gcc cmake autoconf automake

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite.wsgi:application"]
