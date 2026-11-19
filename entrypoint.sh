#!/bin/sh
set -e

echo "==> Waiting for PostgreSQL at $DB_HOST:$DB_PORT ..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.5
done
echo "==> PostgreSQL is up."

echo "==> Running migrations ..."
python manage.py migrate --noinput

echo "==> Collecting static files ..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn ..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --error-logfile -
