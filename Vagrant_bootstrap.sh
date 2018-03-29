#!/bin/bash

# Dependencies
apt-get update
apt-get install -y software-properties-common
apt-get install -y python-software-properties
apt-get install -y curl
apt-get install -y apt-transport-https
add-apt-repository -y ppa:jonathonf/python-3.6
echo "deb http://download.rethinkdb.com/apt xenial main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
apt-get update

# Python3.6
apt-get install -y python3.6
apt-get install -y python3.6-dev
apt-get install -y build-essential
curl -s https://bootstrap.pypa.io/get-pip.py | python3.6 -
python3.6 -m pip install -r /vagrant/requirements.txt
python3.6 -m pip install -r /vagrant/requirements-ci.txt
python3.6 -m pip install gunicorn

# RethinkDB
apt-get install -y rethinkdb

tee /etc/rethinkdb/instances.d/rethinkdb.conf <<EOF
runuser=root
rungroup=root
bind=0.0.0.0
driver-port=28016
http-port=28010
EOF

service rethinkdb restart

# development environment variables
tee /root/.bashrc <<EOF
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s checkwinsize

if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '

test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'

export LOG_LEVEL=DEBUG
export SERVER_NAME="pysite.local"
export WEBPAGE_PORT="80"
export WEBPAGE_SECRET_KEY="123456789abcdefghijklmn"
export RETHINKDB_HOST="127.0.0.1"
export RETHINKDB_PORT="28016"
export RETHINKDB_DATABASE="database"
export RETHINKDB_TABLE="table"
export BOT_API_KEY="abcdefghijklmnopqrstuvwxyz"
export TEMPLATES_AUTO_RELOAD="yes"
export PREFERRED_URL_SCHEME="http"
alias python=python3.6
EOF


curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce

curl -L https://github.com/docker/compose/releases/download/1.20.0-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose


echo 'docs: https://github.com/discord-python/site/wiki/Development-Environment-(Vagrant)'
