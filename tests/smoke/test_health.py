"""
Smoke tests to verify that the application is up and running.
"""
import pytest
import requests
from utils.config import BASE_URL, API_URL

def test_ui_health():
    """
    Verify that the UI application is accessible.
    """
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"UI application is not accessible. Status code: {response.status_code}"

def test_api_health():
    """
    Verify that the API server is accessible and returns the expected health status.
    """
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200, f"API server is not accessible. Status code: {response.status_code}"
    
    # Verify that the response contains the expected health status
    data = response.json()
    assert "status" in data, "Health endpoint response doesn't contain status field"
    assert data["status"] == "OK", f"Health status is not OK: {data['status']}"

def test_api_version():
    """
    Verify that the API version endpoint returns the expected version information.
    """
    response = requests.get(f"{API_URL}/version")
    assert response.status_code == 200, f"Version endpoint is not accessible. Status code: {response.status_code}"
    
    # Verify that the response contains version information
    data = response.json()
    assert "version" in data, "Version endpoint response doesn't contain version field"
