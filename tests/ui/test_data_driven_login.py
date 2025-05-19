"""
Data-driven UI tests for login functionality.
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import BASE_URL
from utils.data_loader import load_csv_data

# Load test data from CSV file
login_scenarios = load_csv_data("test_login.csv")

@pytest.mark.parametrize("scenario", login_scenarios, ids=[s["scenario"] for s in login_scenarios])
def test_login_scenarios(driver, scenario):
    """
    Test various login scenarios using data-driven approach.
    
    Args:
        driver: WebDriver fixture
        scenario: Dictionary containing login scenario data
    """
    # Extract scenario data
    username = scenario["username"]
    password = scenario["password"]
    expected_result = scenario["expected_result"]
    error_message = scenario.get("error_message", "")
    
    # Initialize page objects
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Navigate to login page
    login_page.open(BASE_URL)
    
    # Perform login
    login_page.login(username, password)
    
    # Verify results based on expected outcome
    if expected_result == "success":
        # Check if dashboard loaded successfully
        assert dashboard_page.is_loaded(), "Dashboard did not load after successful login"
        
        # Verify welcome message contains username
        welcome_message = dashboard_page.get_welcome_message()
        assert username in welcome_message, f"Welcome message doesn't contain username: {welcome_message}"
    else:
        # Check if error message is displayed
        assert login_page.is_error_message_displayed(), "Error message not displayed for invalid login"
        
        # Verify error message content if specified
        if error_message:
            actual_error = login_page.get_error_message()
            assert error_message in actual_error, f"Expected error '{error_message}' but got: {actual_error}"
