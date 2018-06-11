FROM python:3.6-alpine3.7

RUN apk add --update tini \
                     git \
                     build-base \
                     gcc \
                     cmake \
                     autoconf \
                     automake \
                     libtool \
                     ruby \
                     ruby-dev \
                     ruby-rdoc \
                     ruby-irb \
                     docker \
                     curl

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1

RUN pip install pipenv
RUN gem install scss_lint
