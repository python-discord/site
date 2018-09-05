FROM pythondiscord/django AS builder

ENV DATABASE_URL postgres://user:pass@host/db
ENV SECRET_KEY unused

RUN mkdir -p /var/www/pythondiscord.com

RUN python3 manage.py collectstatic --noinput


## NGINX setup
# Copy over only the static files from the previous stage
# to ensure a minimal image size in our NGINX container.
FROM nginx:alpine

COPY --from=builder /var/www/pythondiscord.com /var/www/pythondiscord.com

CMD ["nginx", "-g", "daemon off;"]
