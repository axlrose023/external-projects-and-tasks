#!/bin/bash

# Wait for the database to start
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started."

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create a superuser if it doesn't exist
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; \
      User = get_user_model(); \
      User.objects.filter(email='admin@do.gov.ua').exists() or \
      User.objects.create_superuser('admin', 'admin@do.gov.ua', 'admin')" | python manage.py shell

# Start the Django development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
