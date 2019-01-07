FROM python:3.6-alpine3.7

RUN apk add --update tini
RUN apk add --update git
RUN apk add --update build-base
RUN apk add --update gcc
RUN apk add --update cmake
RUN apk add --update autoconf
RUN apk add --update automake
RUN apk add --update libtool

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1
