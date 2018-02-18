#!/bin/bash

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

# Configs
tee /root/.profile <<EOF
if [ "$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi
fi

export LOG_LEVEL=DEBUG
export SERVER_NAME="pysite.local"
export WEBPAGE_PORT="80"
export WEBPAGE_SECRET_KEY="123456789abcdefghijklmn"
export RETHINKDB_HOST="127.0.0.1"
export RETHINKDB_PORT="28016"
export RETHINKDB_DATABASE="database"
export RETHINKDB_TABLE="table"
export BOT_API_KEY="abcdefghijklmnopqrstuvwxyz"
alias python=python3.6

mesg n || true
EOF

source /root/.profile

echo '
SET YOUR HOSTS FILE TO INCLUDE: 10.1.0.2 pysite.local
vagrant ssh
sudo su
cd /vagrant
gunicorn -w 1 -b 0.0.0.0:80 -c gunicorn_config.py --log-level debug -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker app:app
or
python app.py
in browser: http://pysite.local/
'
