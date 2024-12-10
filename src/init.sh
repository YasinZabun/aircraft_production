#!/bin/bash

echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
    sleep 1
done
echo "Database is ready!"

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
EOF

echo "Populating initial models..."
python manage.py loaddata initial_data.json

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running unit tests."
python manage.py test aircraft_app.apps.accounts.tests
python manage.py test aircraft_app.apps.aircraft.tests
python manage.py test aircraft_app.apps.parts.tests
python manage.py test aircraft_app.apps.teams.tests

exec "$@"
