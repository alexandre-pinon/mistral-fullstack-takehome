#!/bin/bash

export ENV_FILE="tests/.env.integration"
uv run pytest tests/
unset ENV_FILE