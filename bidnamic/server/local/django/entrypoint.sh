#!/bin/sh


echo "Connecting to postgres database..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Connected to postgres database successfully"


python manage.py migrate
python manage.py collectstatic --no-input

echo Starting the server.

gunicorn bidnamic.wsgi:application --bind 0.0.0.0:8000 --workers 4
