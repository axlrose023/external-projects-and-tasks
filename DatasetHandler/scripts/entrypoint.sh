#!/bin/sh
set -e

echo "APP:      Running alembic migrations..."
alembic -c alembic.ini upgrade head

echo "APP:      Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
