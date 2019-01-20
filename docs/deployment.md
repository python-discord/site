# Deployment
The default Dockerfile should do a good job at running a solid web server that
automatically adjusts its worker count based on traffic. This is managed by
uWSGI. You need to configure the `DATABASE_URL` and `SECRET_KEY` variables. If
you want to deploy to a different host than the default, configure the
`ALLOWED_HOSTS` variable.

## Static file hosting
You can either collect the static files in the container and use uWSGI to host
them, or put them on your host and manage them through a web server running on
the host like nginx.

## Database migrations
To bring the schema up-to-date, first stop an existing database container, then
start a container that just runs the migrations and exits, and then starts the
main container off the new container again.

## Ansible task
An example Ansible task to deploy the site is shown below, it should read fairly
humanly and give you a rough idea of steps needed to deploy the site.

```yml
---
- name: ensure the `{{ pysite_pg_username }}` postgres user exists
  become: yes
  become_user: postgres
  postgresql_user:
    name: "{{ pysite_pg_username }}"
    password: "{{ pysite_pg_password }}"
  when: pysite_pg_host == 'localhost'

- name: ensure the `{{ pysite_pg_database }}` postgres database exists
  become: yes
  become_user: postgres
  postgresql_db:
    name: "{{ pysite_pg_database }}"
    owner: "{{ pysite_pg_username }}"
  when: pysite_pg_host == 'localhost'

- name: ensure the `{{ pysite_hub_repository }}` image is up-to-date
  become: yes
  docker_image:
    name: "{{ pysite_hub_repository }}"
    force: yes

- name: ensure the nginx HTTP vhosts are up-to-date
  become: yes
  template:
    src: "nginx/{{ item.key }}.http.conf.j2"
    dest: "/etc/nginx/sites-available/{{ item.value }}.http.conf"
  with_dict: "{{ pysite_domains }}"
  notify: reload nginx

- name: ensure the nginx HTTPS vhosts are up-to-date
  become: yes
  template:
    src: "nginx/{{ item.key }}.https.conf.j2"
    dest: "/etc/nginx/sites-available/{{ item.value }}.https.conf"
  with_dict: "{{ pysite_domains }}"
  notify: reload nginx

- name: ensure the nginx HTTP vhosts are symlinked to `/etc/nginx/sites-enabled`
  become: yes
  file:
    src: /etc/nginx/sites-available/{{ item.value }}.http.conf
    dest: /etc/nginx/sites-enabled/{{ item.value }}.http.conf
    state: link
  with_dict: "{{ pysite_domains }}"
  notify: reload nginx

- name: ensure we have HTTPS certificates
  include_role:
    name: thefinn93.letsencrypt
  vars:
    letsencrypt_cert_domains: "{{ pysite_domains | dict2items | map(attribute='value') | list }}"
    letsencrypt_email: "webmaster@example.com"
    letsencrypt_renewal_command_args: '--renew-hook "systemctl restart nginx"'
    letsencrypt_webroot_path: /var/www/_letsencrypt

- name: ensure the nginx HTTPS vhosts are symlinked to `/etc/nginx/sites-enabled`
  become: yes
  file:
    src: /etc/nginx/sites-available/{{ item.value }}.https.conf
    dest: /etc/nginx/sites-enabled/{{ item.value }}.https.conf
    state: link
  with_dict: "{{ pysite_domains }}"
  notify: reload nginx

- name: ensure the web container is absent
  become: yes
  docker_container:
    name: pysite
    state: absent

- name: ensure the `{{ pysite_static_file_dir }}` directory exists
  become: yes
  file:
    path: "{{ pysite_static_file_dir }}"
    state: directory
    owner: root
    group: root

- name: collect static files
  become: yes
  docker_container:
    image: "{{ pysite_hub_repository }}"
    name: pysite-static-file-writer
    command: python manage.py collectstatic --noinput
    detach: no
    cleanup: yes
    network_mode: host
    env:
      DATABASE_URL: "{{ pysite_pg_database_url }}"
      SECRET_KEY: "me-dont-need-no-secret-key"
      STATIC_ROOT: "/html"
    volumes:
      - "/var/www/pythondiscord.com:/html"

- name: ensure the database schema is up-to-date
  become: yes
  docker_container:
    image: "{{ pysite_hub_repository }}"
    name: pysite-migrator
    detach: no
    cleanup: yes
    command: python manage.py migrate
    network_mode: host
    env:
      DATABASE_URL: "postgres://{{ pysite_pg_username }}:{{ pysite_pg_password }}@{{ pysite_pg_host }}/{{ pysite_pg_database }}"
      SECRET_KEY: "me-dont-need-no-secret-key"

- name: ensure the website container is started
  become: yes
  docker_container:
    image: "{{ pysite_hub_repository }}"
    name: pysite
    network_mode: host
    restart: yes
    restart_policy: unless-stopped
    ports:
      - "127.0.0.1:4000:4000"
    env:
      ALLOWED_HOSTS: "{{ pysite_domains | dict2items | map(attribute='value') | join(',') }}"
      DATABASE_URL: "postgres://{{ pysite_pg_username }}:{{ pysite_pg_password }}@{{ pysite_pg_host }}/{{ pysite_pg_database }}"
      PARENT_HOST: pysite.example.com
      SECRET_KEY: "{{ pysite_secret_key }}"
```
