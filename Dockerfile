FROM python:3.7-alpine

RUN apk add python3-dev git libpq postgresql-dev gcc cmake autoconf automake musl-dev
RUN python3 -m pip install pipenv

ENV PIPENV_HIDE_EMOJIS=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_MAX_SUBPROCESS=2
ENV PIPENV_NOSPIN=1
ENV PIPENV_VENV_IN_PROJECT=1

COPY . /app
WORKDIR /app

RUN pipenv install --deploy --system

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:4000", "pysite:wsgi"]