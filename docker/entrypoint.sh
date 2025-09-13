#!/bin/sh
set -e

until pg_isready -h db -p 5432; do
  echo "Waiting for database..."
  sleep 1
done

python manage.py migrate_schemas --shared --noinput
exec python manage.py runserver 0.0.0.0:8000

