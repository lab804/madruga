#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z stations-db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

pip install -e git+https://$GITTOKEN:@github.com/lab804/labmet_libraries.git@master#egg=labmet_libraries

gunicorn -b 0.0.0.0:5000 manage:app
