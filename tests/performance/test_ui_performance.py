"""
Performance tests for UI response times.
"""
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.transfer_page import TransferPage
from utils.config import BASE_URL, USERNAME, PASSWORD

# Define performance thresholds (in seconds)
UI_PERFORMANCE_THRESHOLDS = {
    "login_page_load": 3.0,
    "login_submit": 4.0,
    "dashboard_load": 5.0,
    "transfer_page_load": 3.0,
    "transfer_submit": 5.0
}

@pytest.mark.performance
def test_login_page_load_performance(driver):
    """
    Test login page load performance.
    """
    login_page = LoginPage(driver)
    
    # Measure the time to load the login page
    start_time = time.time()
    login_page.open(BASE_URL)
    end_time = time.time()
    
    load_time = end_time - start_time
    
    print(f"\nLogin page load time: {load_time:.3f} seconds")
    assert load_time <= UI_PERFORMANCE_THRESHOLDS["login_page_load"], \
        f"Login page load time ({load_time:.3f}s) exceeds threshold ({UI_PERFORMANCE_THRESHOLDS['login_page_load']}s)"

@pytest.mark.performance
def test_login_submission_performance(driver):
    """
    Test login form submission performance.
    """
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Open login page
    login_page.open(BASE_URL)
    
    # Measure the time to submit the login form and load the dashboard
    start_time = time.time()
    login_page.login(USERNAME, PASSWORD)
    
    # Wait for dashboard to load
    WebDriverWait(driver, 10).until(lambda d: dashboard_page.is_loaded())
    end_time = time.time()
    
    login_time = end_time - start_time
    
    print(f"\nLogin submission and dashboard load time: {login_time:.3f} seconds")
    assert login_time <= UI_PERFORMANCE_THRESHOLDS["login_submit"], \
        f"Login submission time ({login_time:.3f}s) exceeds threshold ({UI_PERFORMANCE_THRESHOLDS['login_submit']}s)"

@pytest.mark.performance
def test_dashboard_load_performance(logged_in_driver):
    """
    Test dashboard page load performance (after already logged in).
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    
    # Navigate directly to the dashboard
    start_time = time.time()
    driver.get(f"{BASE_URL}/dashboard")
    
    # Wait for dashboard to load
    WebDriverWait(driver, 10).until(lambda d: dashboard_page.is_loaded())
    end_time = time.time()
    
    load_time = end_time - start_time
    
    print(f"\nDashboard load time: {load_time:.3f} seconds")
    assert load_time <= UI_PERFORMANCE_THRESHOLDS["dashboard_load"], \
        f"Dashboard load time ({load_time:.3f}s) exceeds threshold ({UI_PERFORMANCE_THRESHOLDS['dashboard_load']}s)"

@pytest.mark.performance
def test_transfer_page_load_performance(logged_in_driver):
    """
    Test transfer page load performance.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Ensure dashboard is loaded
    assert dashboard_page.is_loaded(), "Dashboard did not load for transfer page test"
    
    # Measure time to load the transfer page
    start_time = time.time()
    dashboard_page.click_transfer()
    
    # Wait for transfer page to load
    WebDriverWait(driver, 10).until(lambda d: transfer_page.is_loaded())
    end_time = time.time()
    
    load_time = end_time - start_time
    
    print(f"\nTransfer page load time: {load_time:.3f} seconds")
    assert load_time <= UI_PERFORMANCE_THRESHOLDS["transfer_page_load"], \
        f"Transfer page load time ({load_time:.3f}s) exceeds threshold ({UI_PERFORMANCE_THRESHOLDS['transfer_page_load']}s)"

@pytest.mark.performance
def test_transfer_submission_performance(logged_in_driver):
    """
    Test transfer form submission performance.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    assert transfer_page.is_loaded(), "Transfer page did not load for submission test"
    
    # Measure time to submit the transfer form
    start_time = time.time()
    transfer_page.perform_transfer(
        from_account="12345678",
        to_account="87654321",
        amount=100,
        description="Performance test transfer"
    )
    
    # Wait for success message
    WebDriverWait(driver, 10).until(
        lambda d: "Transfer successful" in transfer_page.get_success_message()
    )
    end_time = time.time()
    
    submission_time = end_time - start_time
    
    print(f"\nTransfer submission time: {submission_time:.3f} seconds")
    assert submission_time <= UI_PERFORMANCE_THRESHOLDS["transfer_submit"], \
        f"Transfer submission time ({submission_time:.3f}s) exceeds threshold ({UI_PERFORMANCE_THRESHOLDS['transfer_submit']}s)"
