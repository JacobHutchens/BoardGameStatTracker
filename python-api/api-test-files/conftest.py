"""
Shared pytest fixtures and helper functions for API tests.
"""
import os
import pytest
import requests
from typing import Optional


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for API requests from BASE_URL environment variable."""
    url = os.getenv("BASE_URL", "http://localhost:8000/v1")
    if not url.endswith("/"):
        url += "/"
    return url.rstrip("/")


@pytest.fixture(scope="session")
def http_client():
    """HTTP client session for making requests."""
    session = requests.Session()
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    yield session
    session.close()


@pytest.fixture(scope="function")
def user_token(http_client, base_url) -> Optional[str]:
    """
    User authentication token fixture.
    Logs in using TEST_USER_EMAIL and TEST_USER_PASSWORD from environment.
    """
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    
    if not email or not password:
        pytest.skip("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set")
    
    response = http_client.post(
        f"{base_url}/auth/login",
        json={"emailOrUsername": email, "password": password}
    )
    
    if response.status_code != 200:
        pytest.skip(f"User login failed: {response.status_code}")
    
    data = response.json()
    return data.get("accessToken")


@pytest.fixture(scope="function")
def publisher_token(http_client, base_url) -> Optional[str]:
    """
    Publisher authentication token fixture.
    Logs in using TEST_PUBLISHER_EMAIL and TEST_PUBLISHER_PASSWORD from environment.
    """
    email = os.getenv("TEST_PUBLISHER_EMAIL")
    password = os.getenv("TEST_PUBLISHER_PASSWORD")
    
    if not email or not password:
        pytest.skip("TEST_PUBLISHER_EMAIL and TEST_PUBLISHER_PASSWORD must be set")
    
    response = http_client.post(
        f"{base_url}/auth/publisher/login",
        json={"emailOrUsername": email, "password": password}
    )
    
    if response.status_code != 200:
        pytest.skip(f"Publisher login failed: {response.status_code}")
    
    data = response.json()
    return data.get("accessToken")


@pytest.fixture(scope="function")
def authenticated_user_client(http_client, user_token):
    """HTTP client with user authentication token set."""
    http_client.headers.update({
        "Authorization": f"Bearer {user_token}"
    })
    yield http_client
    http_client.headers.pop("Authorization", None)


@pytest.fixture(scope="function")
def authenticated_publisher_client(http_client, publisher_token):
    """HTTP client with publisher authentication token set."""
    http_client.headers.update({
        "Authorization": f"Bearer {publisher_token}"
    })
    yield http_client
    http_client.headers.pop("Authorization", None)


def make_authenticated_request(
    http_client,
    method: str,
    url: str,
    token: Optional[str] = None,
    **kwargs
) -> requests.Response:
    """
    Helper function to make an authenticated request.
    
    Args:
        http_client: Requests session
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        token: Optional Bearer token (if None, uses existing Authorization header)
        **kwargs: Additional arguments passed to requests method
    
    Returns:
        Response object
    """
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    method_func = getattr(http_client, method.lower())
    return method_func(url, headers=headers, **kwargs)


def validate_response_shape(response: requests.Response, expected_keys: list, nested_validation: dict = None):
    """
    Validate response JSON structure and types.
    
    Args:
        response: Response object
        expected_keys: List of top-level keys that must be present
        nested_validation: Dict mapping nested paths to expected types/structures
    """
    assert response.status_code < 400, f"Expected success status, got {response.status_code}"
    
    data = response.json()
    
    # Validate top-level keys
    for key in expected_keys:
        assert key in data, f"Missing expected key: {key}"
    
    # Validate nested structures if provided
    if nested_validation:
        for path, expected_type in nested_validation.items():
            keys = path.split(".")
            value = data
            for key in keys:
                assert key in value, f"Missing nested key: {path}"
                value = value[key]
            
            if isinstance(expected_type, type):
                assert isinstance(value, expected_type), f"Expected {expected_type} for {path}, got {type(value)}"
            elif isinstance(expected_type, list):
                assert isinstance(value, list), f"Expected list for {path}, got {type(value)}"
                if expected_type and isinstance(expected_type[0], dict):
                    # Validate list items have expected structure
                    for item in value:
                        for item_key in expected_type[0].keys():
                            assert item_key in item, f"Missing key {item_key} in {path} item"
