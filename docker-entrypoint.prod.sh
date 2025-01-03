#!/bin/bash

# Wait for database to be ready
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for database connection..."
  sleep 2
done

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

exec "$@" 