#!/bin/bash

# stop on error
set -e

host="$DB_CONTAINER_NAME"
user="$POSTGRES_USER"
db="$POSTGRES_DB"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$user" -d "$db" -c '\q'; do
  >&2 echo "Postgres at $host:5432/$db is unavailable - sleeping"
  sleep 1
done

>&1 echo "Postgres is up - executing command"
exec "$@"
