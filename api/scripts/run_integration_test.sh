#!/bin/bash

export DATABASE_URL="postgresql+asyncpg://test_user:test_password@localhost:5433/test_db"
uv run pytest tests/
unset DATABASE_URL