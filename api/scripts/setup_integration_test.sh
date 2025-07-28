#!/bin/bash

docker compose -f tests/compose.integration.yaml up -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 1
docker compose -f tests/compose.integration.yaml exec -T test-db pg_isready -U test_user -d test_db

while [ $? -ne 0 ]; do
    echo "Database not ready yet, waiting..."
    sleep 1
    docker compose -f tests/compose.integration.yaml exec -T test-db pg_isready -U test_user -d test_db
done
echo "Database is ready! Running migrations..."

export ENV_FILE="tests/.env.integration"
uv run alembic upgrade head
unset ENV_FILE