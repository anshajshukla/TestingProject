"""
UI tests for negative scenarios and error handling.
"""
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL, USERNAME, PASSWORD

def test_session_timeout(driver):
    """
    Test that the session times out after inactivity period.
    """
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Login to the application
    login_page.open(BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    
    # Verify successful login
    assert dashboard_page.is_loaded(), "Dashboard did not load after login"
    
    # Wait for session timeout (this is a simplification and would need to be adjusted)
    # In a real application, you might want to mock the timeout or use a test environment
    # with a shorter timeout setting
    print("Waiting for session timeout...")
    time.sleep(5)  # Simulating wait for timeout
    
    # Try to access a protected page after timeout
    driver.get(f"{BASE_URL}/accounts")
    
    # Verify that we are redirected to login page
    assert "login" in driver.current_url.lower(), "Not redirected to login page after session timeout"

def test_browser_back_button(logged_in_driver):
    """
    Test application behavior when using browser back button after logout.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    
    # Verify we're logged in
    assert dashboard_page.is_loaded(), "Dashboard did not load after login"
    
    # Logout
    dashboard_page.logout()
    
    # Verify logout (check if we're on the login page)
    assert "login" in driver.current_url.lower(), "Not redirected to login page after logout"
    
    # Use browser back button
    driver.back()
    
    # Verify that we don't have access to dashboard (should be redirected to login)
    # Wait a moment for any redirects to occur
    time.sleep(2)
    
    # Verify URL contains 'login' indicating we've been redirected
    assert "login" in driver.current_url.lower(), "Back button allowed access to protected page after logout"

def test_multiple_login_attempts(driver):
    """
    Test account lockout after multiple failed login attempts.
    """
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Attempt to login with invalid credentials multiple times
    for i in range(5):  # Assume account locks after 5 failed attempts
        login_page.login("invalid_user", "invalid_password")
        
        # Check for error message
        assert login_page.is_error_message_displayed(), f"Error message not displayed on attempt {i+1}"
        
        # On the last attempt, check for account lockout message
        if i == 4:
            error_message = login_page.get_error_message()
            assert "account locked" in error_message.lower() or "too many attempts" in error_message.lower(), \
                f"Account not locked after 5 failed attempts. Message: {error_message}"

def test_xss_vulnerability(driver):
    """
    Test for potential XSS vulnerabilities in form inputs.
    """
    login_page = LoginPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Attempt XSS attack through login form
    xss_script = "<script>alert('XSS')</script>"
    login_page.enter_username(xss_script)
    login_page.enter_password(PASSWORD)
    login_page.click_login()
    
    # Check if the script was executed by looking for alert dialog
    # This will only work if the site is vulnerable to XSS
    # In a secure application, this should NOT find an alert
    try:
        alert = driver.switch_to.alert
        alert.accept()
        pytest.fail("XSS vulnerability detected: Script executed and alert displayed")
    except:
        # No alert found - this is the expected secure behavior
        pass
    
    # Verify that either we see an error message or we're still on the login page
    assert "login" in driver.current_url.lower() or login_page.is_error_message_displayed(), \
        "Neither remained on login page nor displayed error after XSS attempt"
