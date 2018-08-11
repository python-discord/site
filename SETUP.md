# Setting up & running up the website locally
*to be put on the wiki*

- `pipenv sync`
- `psql -c 'CREATE USER pysite;'`
- `psql -c 'CREATE DATABASE pysite OWNER pysite;'`
- `echo 'DEBUG=1' >> .env`
- `echo 'DATABASE_URL=postgres://pysite:@localhost/pysite' >> .env`
- `pipenv shell`
- `python manage.py migrate`
- `python manage.py runserver`
