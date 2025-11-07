#!/usr/bin/env bash
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
    sleep 0.5
  done
fi

python manage.py migrate --noinput

echo "Loading initial CV data…"
python manage.py loaddata cv --verbosity=1 || true


exec python manage.py runserver 0.0.0.0:8000
