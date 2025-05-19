"""
UI tests for fund transfer functionality.
"""
import pytest
from pages.dashboard_page import DashboardPage
from pages.transfer_page import TransferPage
from utils.config import BASE_URL

def test_successful_transfer(logged_in_driver):
    """
    Test successful fund transfer between accounts.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Get initial account balance for verification later
    initial_balance = dashboard_page.get_account_balance()
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    
    # Verify transfer page is loaded
    assert transfer_page.is_loaded(), "Transfer page did not load"
    
    # Perform transfer
    transfer_page.perform_transfer(
        from_account="12345678",  # Sample account numbers
        to_account="87654321",
        amount=100,
        description="Test transfer"
    )
    
    # Verify success message
    success_message = transfer_page.get_success_message()
    assert "Transfer successful" in success_message, f"Unexpected success message: {success_message}"
    
    # Navigate back to dashboard to verify updated balance
    driver.get(f"{BASE_URL}/dashboard")
    assert dashboard_page.is_loaded(), "Dashboard did not load after transfer"
    
    # Get updated balance - Note: This is a simplified check and would need to be adjusted
    # for the actual application's behavior regarding balance formatting
    updated_balance = dashboard_page.get_account_balance()
    assert updated_balance != initial_balance, "Account balance did not change after transfer"

def test_transfer_invalid_amount(logged_in_driver):
    """
    Test transfer with invalid amount is rejected.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    
    # Verify transfer page is loaded
    assert transfer_page.is_loaded(), "Transfer page did not load"
    
    # Attempt transfer with negative amount
    transfer_page.select_from_account("12345678")
    transfer_page.select_to_account("87654321")
    transfer_page.enter_amount(-100)
    transfer_page.click_transfer()
    
    # Verify error message
    error_message = transfer_page.get_error_message()
    assert "Amount must be positive" in error_message, f"Unexpected error message: {error_message}"
    
    # Attempt transfer with zero amount
    transfer_page.enter_amount(0)
    transfer_page.click_transfer()
    
    # Verify error message
    error_message = transfer_page.get_error_message()
    assert "Amount must be positive" in error_message, f"Unexpected error message: {error_message}"

def test_transfer_insufficient_funds(logged_in_driver):
    """
    Test transfer with insufficient funds is rejected.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    
    # Verify transfer page is loaded
    assert transfer_page.is_loaded(), "Transfer page did not load"
    
    # Attempt transfer with amount exceeding available balance
    transfer_page.perform_transfer(
        from_account="12345678",
        to_account="87654321",
        amount=1000000,  # Assume this is more than available balance
        description="Test insufficient funds"
    )
    
    # Verify error message
    error_message = transfer_page.get_error_message()
    assert "Insufficient funds" in error_message, f"Unexpected error message: {error_message}"

def test_transfer_same_account(logged_in_driver):
    """
    Test transfer to the same account is rejected.
    """
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    
    # Verify transfer page is loaded
    assert transfer_page.is_loaded(), "Transfer page did not load"
    
    # Attempt transfer to the same account
    account_number = "12345678"
    transfer_page.perform_transfer(
        from_account=account_number,
        to_account=account_number,
        amount=100,
        description="Test same account transfer"
    )
    
    # Verify error message
    error_message = transfer_page.get_error_message()
    assert "Cannot transfer to the same account" in error_message, f"Unexpected error message: {error_message}"
