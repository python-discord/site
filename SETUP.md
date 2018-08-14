# Setting up & running up the website locally
*to be put on the wiki*

- `pipenv sync`
- `psql -c 'CREATE USER pysite WITH CREATEDB;'`
- `psql -c 'CREATE DATABASE pysite OWNER pysite;'`
- `echo 'DEBUG=1' >> .env`
- `echo 'DATABASE_URL=postgres://pysite:@localhost/pysite' >> .env`
- `echo 'BOT_API_KEY=123456' >> .env`
- `pipenv shell`
- `python manage.py migrate`
- `python manage.py runserver`
