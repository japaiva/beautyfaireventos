#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
RETRIES=10
until psql $DATABASE_URL -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for PostgreSQL server, $((RETRIES--)) remaining attempts..."
  sleep 5
done

# Create schema if it doesn't exist
echo "Ensuring schema 'bfcongressos' exists..."
psql $DATABASE_URL -c "CREATE SCHEMA IF NOT EXISTS bfcongressos;" > /dev/null 2>&1

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start server
echo "Starting server..."
exec "$@"
