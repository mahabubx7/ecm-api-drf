#!/bin/bash

# Wait for postgres
while ! nc -z db 5432; do
  echo "🟡 Waiting for postgres..."
  sleep 1
done
echo "✅ PostgreSQL started"

# Make migrations for each app in the correct order
python manage.py makemigrations common
python manage.py makemigrations users
python manage.py makemigrations products
python manage.py makemigrations cart
python manage.py makemigrations orders
python manage.py makemigrations authentication

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8020 --workers 3 