# How to set up the development environment

This uses vagrant and virtualbox, but it is entirely optional. You can install all the prerequisites directly on your computer.

# Starting point

Go the root of this project

## Booting the VM

Start by installing the prerequisites:

- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

### Hosts file

Next put these values in your hosts file

```bash
10.1.0.2    pysite.local
10.1.0.2    api.pysite.local
```

you will typically find the hosts file here: `C:\Windows\System32\drivers\etc\hosts` or here `/etc/hosts`

> You need administrative or root privileges to edit a hosts file

### Booting the VM

Once installed, open your favorite terminal and type

```bash
vagrant ssh
sudo su
cd /vagrant
gunicorn -w 1 -b 0.0.0.0:80 -c gunicorn_config.py --log-level debug -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker app:app
# or
python app.py
```

Now open your browser and navigate to `http://pysite.local/`

### Environment Variables

The vagrantfile includes the necessary dummy environment variables to run the flask app

### Changing code

Any code you change outside the virtual machine is sync'd with the /vagrant folder inside the VM, so there is no need to copy files in manually.
