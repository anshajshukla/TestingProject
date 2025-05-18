"""
UI tests for the login functionality.
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL, USERNAME, PASSWORD

def test_valid_login(driver):
    """
    Test login with valid credentials.
    """
    # Initialize page objects
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Perform login
    login_page.login(USERNAME, PASSWORD)
    
    # Verify that login was successful by checking dashboard is loaded
    assert dashboard_page.is_loaded(), "Dashboard did not load after login"
    
    # Verify welcome message contains username
    welcome_message = dashboard_page.get_welcome_message()
    assert USERNAME in welcome_message, f"Welcome message doesn't contain username. Message: {welcome_message}"

def test_invalid_login(driver):
    """
    Test login with invalid credentials.
    """
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Try to login with invalid credentials
    login_page.login("invalid_user", "invalid_password")
    
    # Verify that error message is displayed
    assert login_page.is_error_message_displayed(), "Error message not displayed for invalid login"
    
    # Verify error message content
    error_message = login_page.get_error_message()
    assert "Invalid credentials" in error_message, f"Unexpected error message: {error_message}"

def test_empty_credentials(driver):
    """
    Test login with empty credentials.
    """
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Try to login with empty credentials
    login_page.login("", "")
    
    # Verify that error message is displayed
    assert login_page.is_error_message_displayed(), "Error message not displayed for empty credentials"
    
    # Verify error message content
    error_message = login_page.get_error_message()
    assert "Username and password are required" in error_message, f"Unexpected error message: {error_message}"

def test_forgot_password_link(driver):
    """
    Test that forgot password link redirects to the correct page.
    """
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Click forgot password link
    login_page.click_forgot_password()
    
    # Verify URL contains forgot-password
    assert "forgot-password" in driver.current_url, f"URL does not contain forgot-password: {driver.current_url}"
