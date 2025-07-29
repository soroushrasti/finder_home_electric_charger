#!/bin/bash
set -e

echo "Checking environment variables..."

# Use Railway's default DATABASE_URL if custom one isn't set
#if [ -z "$DATABASE_URL_SQLALCHEMY" ]; then
#    if [ -n "$DATABASE_URL" ]; then
#        echo "Using DATABASE_URL as DATABASE_URL_SQLALCHEMY"
#        export DATABASE_URL_SQLALCHEMY="$DATABASE_URL"
#    else
#        echo "ERROR: Neither DATABASE_URL_SQLALCHEMY nor DATABASE_URL environment variable is set"
#        exit 1
#    fi
#fi

echo "Running migrations..."
#poetry run python migrate.py

echo "Starting application..."
exec poetry run python main.py