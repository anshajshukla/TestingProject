"""
Pytest fixtures and configuration for the banking tests project.
"""
import pytest
from utils.driver_factory import get_driver
from utils.config import BASE_URL, API_URL, USERNAME, PASSWORD
import requests

@pytest.fixture(scope="function")
def driver():
    """
    Create and return a WebDriver instance for each test function.
    The driver is automatically closed after the test.
    """
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def api_session():
    """
    Create a requests session for API tests.
    The session is reused across all tests in the session.
    """
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="function")
def authenticated_session(api_session):
    """
    Create an authenticated API session.
    """
    response = api_session.post(
        f"{API_URL}/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if response.status_code == 200:
        token = response.json().get("token")
        api_session.headers.update({"Authorization": f"Bearer {token}"})
    else:
        pytest.fail(f"Failed to authenticate: {response.text}")
    
    return api_session

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Create a WebDriver instance that's already logged in.
    """
    from pages.login_page import LoginPage
    
    login_page = LoginPage(driver)
    login_page.open(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    
    yield driver
