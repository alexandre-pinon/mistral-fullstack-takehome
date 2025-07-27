# Integration Tests

This directory contains integration tests for the API.

## Setup

Install test dependencies:

```bash
uv add --dev pytest pytest-asyncio httpx
```

## Running Tests

Run all tests:

```bash
pytest
```

Run only integration tests:

```bash
pytest -m integration
```

Run only health check tests:

```bash
pytest tests/test_health_integration.py
```

Run with verbose output:

```bash
pytest -v
```

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_health_integration.py` - Integration tests for the health check endpoint

## What the Health Check Tests Do

The integration tests for the health check endpoint:

1. Make actual HTTP requests to the `/health` endpoint
2. Verify the response status code is 200 OK
3. Verify the response JSON structure matches the expected format
4. Check that the response contains the correct content-type header
5. Validate that the response body has the expected `status: "ok"` field
