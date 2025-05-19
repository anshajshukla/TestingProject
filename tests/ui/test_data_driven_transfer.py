"""
Data-driven UI tests for fund transfer functionality.
"""
import pytest
from pages.dashboard_page import DashboardPage
from pages.transfer_page import TransferPage
from utils.config import BASE_URL
from utils.data_loader import load_json_data

# Load test data from JSON file
transfer_data = load_json_data("test_accounts.json")
transfer_scenarios = transfer_data.get("transfer_scenarios", [])

# Create parametrized test using the scenarios
@pytest.mark.parametrize("scenario", transfer_scenarios, ids=[s["name"] for s in transfer_scenarios])
def test_transfer_scenarios(logged_in_driver, scenario):
    """
    Test various transfer scenarios using data-driven approach.
    
    Args:
        logged_in_driver: WebDriver fixture with authenticated session
        scenario: Dictionary containing transfer scenario data
    """
    # Extract scenario data
    from_account = scenario["from_account"]
    to_account = scenario["to_account"]
    amount = scenario["amount"]
    description = scenario["description"]
    expected_result = scenario["expected_result"]
    
    # Initialize page objects
    driver = logged_in_driver
    dashboard_page = DashboardPage(driver)
    transfer_page = TransferPage(driver)
    
    # Navigate to transfer page
    dashboard_page.click_transfer()
    
    # Verify transfer page is loaded
    assert transfer_page.is_loaded(), "Transfer page did not load"
    
    # Perform transfer
    transfer_page.perform_transfer(
        from_account=from_account,
        to_account=to_account,
        amount=amount,
        description=description
    )
    
    # Verify results based on expected outcome
    if expected_result == "success":
        success_message = transfer_page.get_success_message()
        assert "Transfer successful" in success_message, f"Expected success but got: {success_message}"
    else:
        error_message = transfer_page.get_error_message()
        expected_error = scenario.get("error_message", "")
        assert expected_error in error_message, f"Expected error '{expected_error}' but got: {error_message}"
