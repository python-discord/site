FROM python:3.6-alpine3.7

# Install base packages
RUN apk add --update autoconf automake \
                     build-base \
                     cmake curl \
                     docker \
                     gcc git \
                     libtool \
                     nodejs nodejs-npm \
                     ruby ruby-dev ruby-irb ruby-rdoc \
                     tini

# Set up env vars
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1

# Install toolchain
RUN pip install pipenv
RUN gem install scss_lint
RUN npm install -g eslint --save-dev
