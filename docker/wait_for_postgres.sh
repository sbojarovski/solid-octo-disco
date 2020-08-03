#!/bin/bash

# stop on error
set -e

host="$DB_CONTAINER_NAME"
user="$DB_USER"
db="$DB_NAME"
password="$DB_PASSWORD"
port="$DB_PORT"

ssl_required="$DB_SSL_REQUIRED"
ca_cert="$DB_CA_PEM"

>&1 echo $DB_SSL_REQUIRED

if [ -z "$ssl_required" ]
then
      postgres_args="host=$host port=$port user=$user dbname=$db password=$password"
else
      postgres_args="sslmode=verify-ca sslrootcert=$ca_cert host=$host port=$port user=$user dbname=$db password=$password"
fi

>&1 echo $postgres_args

until psql "$postgres_args" -c '\q'; do
  >&2 echo "Postgres at $host:$port/$db is unavailable - sleeping"
  sleep 1
done

>&1 echo "Postgres is up - executing command"
exec "$@"
