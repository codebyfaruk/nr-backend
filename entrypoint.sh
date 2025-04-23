#!/bin/bash

# Wait for PostgreSQL using Python
echo "Waiting for PostgreSQL..."
python << END
import time
import socket

while True:
    try:
        with socket.create_connection(("db", 5432), timeout=1):
            break
    except OSError:
        time.sleep(1)
END
echo "PostgreSQL is up!"

# Run Django migrations
python manage.py migrate

# Collect static files
# python manage.py collectstatic --noinput

# Start development server
python manage.py runserver 0.0.0.0:8000
