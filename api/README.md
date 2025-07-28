## Integration Tests

The `/tests` directory contains integration tests for the API.

### Setup

Install test dependencies:

```bash
uv sync --extra test
```

### Running Tests

The easiest way to run integration tests is using the provided scripts:

**Run the integration tests:**

```bash
./scripts/run_integration_test.sh
```

This script:

- Starts the test database using Docker Compose
- Runs database migrations
- Sets up the test environment
- Runs all tests in the `tests/` directory
- Cleans up the docker compose
