#!/bin/bash

# Run makemigrations and migrate
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Check if superuser 'batman' exists, if not create it
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='batman').exists():
    User.objects.create_superuser('batman', 'batman@example.com', 'yourpassword')
EOF

# Run Gunicorn server
exec gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
