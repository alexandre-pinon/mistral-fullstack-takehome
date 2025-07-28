# Integration Tests

This directory contains integration tests for the API.

## Setup

Install test dependencies:

```bash
uv add --dev pytest pytest-asyncio httpx
```

## Running Tests

### Using the Test Scripts (Recommended)

The easiest way to run integration tests is using the provided scripts:

1. **Setup the test database:**

   ```bash
   ./scripts/setup_integration_test.sh
   ```

   This script:

   - Starts the test database using Docker Compose
   - Runs database migrations
   - Sets up the test environment

2. **Run the integration tests:**
   ```bash
   ./scripts/run_integration_test.sh
   ```
   This script:
   - Sets the test database URL
   - Runs all tests in the `tests/` directory
   - Cleans up environment variables
