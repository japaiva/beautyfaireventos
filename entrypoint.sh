#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
RETRIES=10
until psql $DATABASE_URL -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for PostgreSQL server, $((RETRIES--)) remaining attempts..."
  sleep 5
done

# Create schema if it doesn't exist
# COMENTADO: Usando schema 'public' padrão para simplificar
# echo "Ensuring schema 'bfcongressos' exists..."
# psql $DATABASE_URL -c "CREATE SCHEMA IF NOT EXISTS bfcongressos;" > /dev/null 2>&1

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if environment variables are set
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py shell <<EOF
from core.models import Usuario
if not Usuario.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    Usuario.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        password='$DJANGO_SUPERUSER_PASSWORD',
        first_name='${DJANGO_SUPERUSER_FIRSTNAME:-Admin}',
        last_name='${DJANGO_SUPERUSER_LASTNAME:-User}'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
EOF
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start server
echo "Starting server..."
exec "$@"
