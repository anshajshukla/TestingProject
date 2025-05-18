"""
API tests for authentication endpoints.
"""
import pytest
import requests
from utils.config import API_URL, USERNAME, PASSWORD

def test_login_success(api_session):
    """
    Test successful login with valid credentials.
    """
    response = api_session.post(
        f"{API_URL}/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    assert response.status_code == 200, f"Login failed with status code: {response.status_code}"
    data = response.json()
    assert "token" in data, "Login response doesn't contain token"
    assert data["token"], "Token is empty"

def test_login_failure_invalid_credentials(api_session):
    """
    Test login failure with invalid credentials.
    """
    response = api_session.post(
        f"{API_URL}/login",
        json={"username": "invalid_user", "password": "invalid_password"}
    )
    
    assert response.status_code == 401, f"Expected 401 status code, got: {response.status_code}"
    data = response.json()
    assert "error" in data, "Error message not found in response"
    assert "Invalid credentials" in data["error"], f"Unexpected error message: {data['error']}"

def test_login_failure_missing_fields(api_session):
    """
    Test login failure with missing required fields.
    """
    # Test missing username
    response = api_session.post(
        f"{API_URL}/login",
        json={"password": PASSWORD}
    )
    
    assert response.status_code == 400, f"Expected 400 status code, got: {response.status_code}"
    
    # Test missing password
    response = api_session.post(
        f"{API_URL}/login",
        json={"username": USERNAME}
    )
    
    assert response.status_code == 400, f"Expected 400 status code, got: {response.status_code}"

def test_logout(authenticated_session):
    """
    Test successful logout.
    """
    response = authenticated_session.post(f"{API_URL}/logout")
    
    assert response.status_code == 200, f"Logout failed with status code: {response.status_code}"
    
    # Verify that the token is invalidated by making a request to a protected endpoint
    response = authenticated_session.get(f"{API_URL}/accounts")
    assert response.status_code == 401, "Token was not invalidated after logout"
