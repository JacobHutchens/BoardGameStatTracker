# API Test Suite

This directory contains pytest test files for the Board Game Stat Tracker REST API.

## Overview

The test suite is organized into individual test files, one per API resource:

- `test_auth.py` - Authentication endpoints (login, register, refresh, etc.)
- `test_reference_data.py` - Reference data endpoints (scopes, data-types)
- `test_games.py` - Game management endpoints
- `test_stat_sets.py` - Stat set endpoints (nested under games)
- `test_sessions.py` - Session management endpoints
- `test_users.py` - User profile endpoints
- `test_user_stats.py` - User statistics endpoints
- `test_social.py` - Social features (followers, following, user search)
- `test_feed.py` - Following feed endpoint
- `test_export.py` - Data export endpoints
- `test_publishers.py` - Publisher endpoints (requires publisher authentication)

## Setup

### Prerequisites

- Python 3.7+
- pytest
- requests

Install dependencies:

```bash
pip install pytest requests
```

### Environment Variables

The following environment variables must be set before running tests:

- `BASE_URL` - Base URL for the API (default: `http://localhost:8000/v1`)
- `TEST_USER_EMAIL` - Email for test user account
- `TEST_USER_PASSWORD` - Password for test user account
- `TEST_PUBLISHER_EMAIL` - Email for test publisher account
- `TEST_PUBLISHER_PASSWORD` - Password for test publisher account

Example `.env` file:

```bash
BASE_URL=http://localhost:8000/v1
TEST_USER_EMAIL=testuser@example.com
TEST_USER_PASSWORD=TestPassword123!
TEST_PUBLISHER_EMAIL=publisher@example.com
TEST_PUBLISHER_PASSWORD=PublisherPassword123!
```

## Running Tests

### Run All Tests

```bash
pytest python-api/api-test-files/
```

### Run Specific Test File

```bash
pytest python-api/api-test-files/test_auth.py
```

### Run Specific Test Class

```bash
pytest python-api/api-test-files/test_auth.py::TestAuthLogin
```

### Run Specific Test

```bash
pytest python-api/api-test-files/test_auth.py::TestAuthLogin::test_login_success
```

### Run with Verbose Output

```bash
pytest python-api/api-test-files/ -v
```

### Run with Coverage

```bash
pytest python-api/api-test-files/ --cov=. --cov-report=html
```

## Test Structure

### Fixtures

The `conftest.py` file provides shared fixtures:

- `base_url` - Base URL for API requests (from `BASE_URL` env var)
- `http_client` - HTTP session for making requests
- `user_token` - User authentication token (from login)
- `publisher_token` - Publisher authentication token (from publisher login)
- `authenticated_user_client` - HTTP client with user token set
- `authenticated_publisher_client` - HTTP client with publisher token set

### Test Files

Each test file includes:

- **Fixtures** - Resource creation/cleanup fixtures (where applicable)
- **Positive Tests** - Valid requests with expected success responses
- **Negative Tests** - Invalid requests (404, 400, 409, 422)
- **Auth Tests** - Missing/invalid token tests (401)
- **Query Parameter Tests** - Tests for endpoints with query parameters
- **Deep Validation** - Response shape validation including nested objects

### Helper Functions

The `conftest.py` file provides helper functions:

- `make_authenticated_request()` - Make authenticated requests
- `validate_response_shape()` - Validate response JSON structure and types

## Test Coverage

The test suite covers:

- All API endpoints from the specification
- All HTTP methods (GET, POST, PATCH, DELETE)
- All status codes (200, 201, 204, 400, 401, 403, 404, 409, 422)
- Authentication (user tokens and publisher tokens)
- Query parameters and pagination
- Request/response validation
- Error handling
- Edge cases (duplicates, not found, invalid data)

## Notes

- Reference data endpoints (`/scopes`, `/data-types`) are read-only and do not require fixtures
- Some tests may skip if required test data cannot be created
- Tests clean up created resources where possible
- Publisher endpoints require distinct publisher authentication tokens
- Session limit tests may require specific test user configuration

## Troubleshooting

### Tests Skipping

If tests are skipping, check:

1. Environment variables are set correctly
2. API server is running and accessible at `BASE_URL`
3. Test user and publisher accounts exist and credentials are correct

### Authentication Failures

If authentication tests fail:

1. Verify `TEST_USER_EMAIL` and `TEST_USER_PASSWORD` are correct
2. Verify `TEST_PUBLISHER_EMAIL` and `TEST_PUBLISHER_PASSWORD` are correct
3. Ensure accounts exist in the test database

### Resource Creation Failures

If resource creation fixtures fail:

1. Check API server logs for errors
2. Verify database is accessible and properly configured
3. Ensure test user has necessary permissions
