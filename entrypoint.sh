#!/bin/bash
set -e

echo "Checking environment variables..."

# Use Railway's default DATABASE_URL if custom one isn't set
#if [ -z "$DATABASE_URL" ]; then
#    if [ -n "$DATABASE_URL" ]; then
#        echo "Using DATABASE_URL as DATABASE_URL"
#        export DATABASE_URL="$DATABASE_URL"
#    else
#        echo "ERROR: Neither DATABASE_URL nor DATABASE_URL environment variable is set"
#        exit 1
#    fi
#fi

echo "Running migrations..."
#poetry run python migrate.py

echo "Starting application..."
exec poetry run python main.py