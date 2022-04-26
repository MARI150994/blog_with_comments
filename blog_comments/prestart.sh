#!/bin/sh

echo "Apply migrations"

python manage.py migrate

echo "Finish migrations"

exec "$@"