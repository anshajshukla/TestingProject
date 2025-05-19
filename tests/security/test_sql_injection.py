"""
Tests for SQL injection vulnerabilities in the banking application.
"""
import pytest
import requests
from utils.config import API_URL

def test_sql_injection_login(api_session):
    """
    Test SQL injection vulnerability in login endpoint.
    """
    # Common SQL injection payloads for authentication bypass
    sql_payloads = [
        "' OR '1'='1",
        "admin'--",
        "admin' OR '1'='1'--",
        "' OR 1=1--",
        "' OR 'x'='x",
        "'); DROP TABLE users; --"
    ]
    
    for payload in sql_payloads:
        response = api_session.post(
            f"{API_URL}/login",
            json={"username": payload, "password": "anything"}
        )
        
        # If vulnerable to SQL injection, this might return 200 with a valid token
        # A secure application should reject these payloads
        assert response.status_code != 200, f"SQL Injection vulnerability detected with payload: {payload}"
        
        # Verify that the response contains an error message
        if response.status_code == 401:
            data = response.json()
            assert "error" in data, "Error message not found in response"

def test_sql_injection_account_query(api_session):
    """
    Test SQL injection vulnerability in account query parameters.
    """
    # First login with valid credentials to get authenticated
    response = api_session.post(
        f"{API_URL}/login",
        json={"username": "testuser", "password": "Test@123"}
    )
    
    assert response.status_code == 200, "Failed to authenticate for SQL injection test"
    token = response.json().get("token")
    api_session.headers.update({"Authorization": f"Bearer {token}"})
    
    # SQL injection payloads for data extraction
    sql_payloads = [
        "1 OR 1=1",
        "1; SELECT * FROM accounts",
        "1 UNION SELECT username, password FROM users",
        "1); DROP TABLE accounts; --"
    ]
    
    # Test account endpoint with SQL injection in query parameter
    for payload in sql_payloads:
        response = api_session.get(f"{API_URL}/accounts?id={payload}")
        
        # Verify that the application properly handles malicious input
        # If it returns a 500 server error, it might be vulnerable
        assert response.status_code != 500, f"Potential SQL Injection vulnerability with payload: {payload}"
        
        # Check for data leakage
        if response.status_code == 200:
            data = response.json()
            # Assuming legitimate response should only contain one account
            if "accounts" in data and isinstance(data["accounts"], list):
                # If we get multiple accounts when requesting a specific ID, 
                # this might indicate SQL injection vulnerability
                assert len(data["accounts"]) <= 1, f"Potential data leakage with payload: {payload}"

def test_sql_injection_headers(api_session):
    """
    Test SQL injection vulnerability through HTTP headers.
    """
    # SQL Injection payloads
    sql_payloads = [
        "' OR '1'='1", 
        "1; SELECT * FROM users"
    ]
    
    for payload in sql_payloads:
        # Try SQL injection through User-Agent header
        headers = {"User-Agent": payload}
        response = api_session.get(f"{API_URL}/accounts", headers=headers)
        
        # Check if the application crashes with 500 error
        assert response.status_code != 500, f"Potential SQL Injection vulnerability in headers with payload: {payload}"

def test_blind_sql_injection(api_session):
    """
    Test for blind SQL injection vulnerabilities.
    """
    # Blind SQL injection tests with time delays
    # If the application is vulnerable, these queries might cause noticeable delays
    time_delay_payloads = [
        "1' AND (SELECT COUNT(*) FROM pg_sleep(5))--",  # PostgreSQL
        "1' AND (SELECT 1 FROM (SELECT SLEEP(5))a)--",  # MySQL
        "1'; WAITFOR DELAY '0:0:5'--"  # SQL Server
    ]
    
    for payload in time_delay_payloads:
        start_time = pytest.helpers.time.time()
        
        response = api_session.get(f"{API_URL}/accounts?id={payload}")
        
        end_time = pytest.helpers.time.time()
        execution_time = end_time - start_time
        
        # If execution time is significantly higher than normal, it might indicate vulnerability
        # Note: This is a simplistic check and might give false positives
        assert execution_time < 4.5, f"Potential blind SQL injection vulnerability with payload: {payload}"
