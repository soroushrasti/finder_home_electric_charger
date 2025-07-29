#!/bin/bash
set -e

echo "Checking environment variables..."
if [ -z "$DATABASE_URL_SQLALCHEMY" ]; then
    echo "ERROR: DATABASE_URL_SQLALCHEMY environment variable is not set"
    exit 1
fi

echo "Running migrations..."
poetry run python migrate.py

echo "Starting application..."
exec poetry run python main.py