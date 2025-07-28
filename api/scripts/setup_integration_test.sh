#!/bin/bash

docker compose -f compose.test.yaml up -d

export DATABASE_URL="postgresql+asyncpg://test_user:test_password@localhost:5433/test_db"
uv run alembic upgrade head
unset DATABASE_URL