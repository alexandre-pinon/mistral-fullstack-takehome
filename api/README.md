## Integration Tests

The `/tests` directory contains integration tests for the API.

### Prerequisites

- [uv](https://docs.astral.sh/uv/)

As stated in the doc, you can **install uv** using this command :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

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
