#!/bin/bash

# Dependencies
apt install -y software-properties-common
apt install -y python-software-properties
apt install -y curl

# Python 3.6
add-apt-repository -y ppa:jonathonf/python-3.6

# Rethinkdb
curl -fsSL https://download.rethinkdb.com/apt/pubkey.gpg | apt-key add -
echo "deb http://download.rethinkdb.com/apt xenial main" | tee /etc/apt/sources.list.d/rethinkdb.list

# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install
apt update
apt install -y apt-transport-https
apt install -y docker-ce
apt install -y rethinkdb
apt install -y python3.6
apt install -y python3.6-dev
apt install -y build-essential
apt install -y python3-distutils

# Compose
curl -Ls https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Pip
curl -s https://bootstrap.pypa.io/get-pip.py | python -
curl -s https://bootstrap.pypa.io/get-pip.py | python3 -
curl -s https://bootstrap.pypa.io/get-pip.py | python3.6 -

# Pipenv
python3.6 -m pip install pipenv

# RethinkDB config
tee /etc/rethinkdb/instances.d/rethinkdb.conf <<EOF
runuser=root
rungroup=root
bind=0.0.0.0
driver-port=28015
http-port=28010
EOF

service rethinkdb restart

# Environment variables
cat > /etc/environment <<EOL
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
VIRTUALENV_ALWAYS_COPY=1
PIPENV_VENV_IN_PROJECT=1
PIPENV_IGNORE_VIRTUALENVS=1
SERVER_NAME="pythondiscord.local"
WEBPAGE_PORT="80"
WEBPAGE_SECRET_KEY="123456789abcdefghijklmn"
RETHINKDB_HOST="127.0.0.1"
RETHINKDB_PORT="28015"
RETHINKDB_DATABASE="pythondiscord"
BOT_API_KEY="abcdefghijklmnopqrstuvwxyz"
TEMPLATES_AUTO_RELOAD="yes"
PREFERRED_URL_SCHEME="http"
PYTHONPATH="/vagrant/pysite"
EOL
