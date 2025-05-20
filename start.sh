#!/bin/bash

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if needed..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="batman").exists():
    User.objects.create_superuser("batman", "batman@example.com", "batman")
EOF

echo "Starting Gunicorn server..."
gunicorn ecommerce.wsgi:application
