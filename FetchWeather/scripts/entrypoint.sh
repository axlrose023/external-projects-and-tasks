#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is ready - running migrations"
# Run migrations
uv run alembic upgrade head

echo "Starting FastAPI application"
# Start the application
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
