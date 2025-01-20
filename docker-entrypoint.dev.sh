#!/bin/bash

# Install requirements first
pip install -r requirements.txt

# Wait for postgres
while ! nc -z db 5432; do
  echo "🟡 Waiting for postgres..."
  sleep 1
done
echo "✅ PostgreSQL started"

# Remove old migrations (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create fresh migrations
echo "Creating migrations..."
python manage.py makemigrations common
python manage.py makemigrations users
python manage.py makemigrations products
python manage.py makemigrations cart
python manage.py makemigrations orders
python manage.py makemigrations authentication

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Seed categories & products
echo "Seeding categories & products..."
# python manage.py runscript products.seeders.categories
python manage.py seed_products


# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser('admin@example.com', 'admin')" | python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

exec "$@"
