#!/bin/sh

# Initialize the database
docker compose exec backend flask db init

# Create migrations
docker compose exec backend flask db migrate -m "initial migration"

# Apply the migrations
docker compose exec backend flask migrate