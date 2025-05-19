"""
Performance tests for API response times.
"""
import pytest
import time
import statistics
from utils.config import API_URL
import json

# Define performance thresholds (in seconds)
PERFORMANCE_THRESHOLDS = {
    "login": 1.0,
    "accounts": 0.8,
    "transactions": 1.2,
    "account_details": 0.5
}

# Number of test iterations
TEST_ITERATIONS = 5

@pytest.mark.performance
def test_login_performance(api_session):
    """
    Test login API performance.
    """
    from utils.config import USERNAME, PASSWORD
    
    response_times = []
    
    for _ in range(TEST_ITERATIONS):
        start_time = time.time()
        response = api_session.post(
            f"{API_URL}/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        end_time = time.time()
        
        assert response.status_code == 200, f"Login request failed: {response.text}"
        response_times.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    # Log results
    print(f"\nLogin API performance stats:")
    print(f"  Average: {avg_time:.3f} seconds")
    print(f"  Min: {min_time:.3f} seconds")
    print(f"  Max: {max_time:.3f} seconds")
    
    # Verify against threshold
    assert avg_time <= PERFORMANCE_THRESHOLDS["login"], \
        f"Login API average response time ({avg_time:.3f}s) exceeds threshold ({PERFORMANCE_THRESHOLDS['login']}s)"

@pytest.mark.performance
def test_accounts_list_performance(authenticated_session):
    """
    Test accounts list API performance.
    """
    response_times = []
    
    for _ in range(TEST_ITERATIONS):
        start_time = time.time()
        response = authenticated_session.get(f"{API_URL}/accounts")
        end_time = time.time()
        
        assert response.status_code == 200, f"Accounts request failed: {response.text}"
        response_times.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    # Log results
    print(f"\nAccounts API performance stats:")
    print(f"  Average: {avg_time:.3f} seconds")
    print(f"  Min: {min_time:.3f} seconds")
    print(f"  Max: {max_time:.3f} seconds")
    
    # Verify against threshold
    assert avg_time <= PERFORMANCE_THRESHOLDS["accounts"], \
        f"Accounts API average response time ({avg_time:.3f}s) exceeds threshold ({PERFORMANCE_THRESHOLDS['accounts']}s)"

@pytest.mark.performance
def test_transactions_list_performance(authenticated_session):
    """
    Test transactions list API performance.
    """
    response_times = []
    
    for _ in range(TEST_ITERATIONS):
        start_time = time.time()
        response = authenticated_session.get(f"{API_URL}/transactions")
        end_time = time.time()
        
        assert response.status_code == 200, f"Transactions request failed: {response.text}"
        response_times.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    # Log results
    print(f"\nTransactions API performance stats:")
    print(f"  Average: {avg_time:.3f} seconds")
    print(f"  Min: {min_time:.3f} seconds")
    print(f"  Max: {max_time:.3f} seconds")
    
    # Verify against threshold
    assert avg_time <= PERFORMANCE_THRESHOLDS["transactions"], \
        f"Transactions API average response time ({avg_time:.3f}s) exceeds threshold ({PERFORMANCE_THRESHOLDS['transactions']}s)"

@pytest.mark.performance
def test_account_details_performance(authenticated_session):
    """
    Test account details API performance.
    """
    # First get all accounts
    accounts_response = authenticated_session.get(f"{API_URL}/accounts")
    accounts = accounts_response.json().get("accounts", [])
    
    if not accounts:
        pytest.skip("No accounts available to test performance")
    
    account_id = accounts[0]["id"]
    response_times = []
    
    for _ in range(TEST_ITERATIONS):
        start_time = time.time()
        response = authenticated_session.get(f"{API_URL}/accounts/{account_id}")
        end_time = time.time()
        
        assert response.status_code == 200, f"Account details request failed: {response.text}"
        response_times.append(end_time - start_time)
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    min_time = min(response_times)
    
    # Log results
    print(f"\nAccount details API performance stats:")
    print(f"  Average: {avg_time:.3f} seconds")
    print(f"  Min: {min_time:.3f} seconds")
    print(f"  Max: {max_time:.3f} seconds")
    
    # Verify against threshold
    assert avg_time <= PERFORMANCE_THRESHOLDS["account_details"], \
        f"Account details API average response time ({avg_time:.3f}s) exceeds threshold ({PERFORMANCE_THRESHOLDS['account_details']}s)"

def save_performance_results(results_dict):
    """
    Save performance test results to a JSON file.
    """
    import os
    import datetime
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports/performance", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/performance/api_performance_{timestamp}.json"
    
    # Save results to file
    with open(filename, 'w') as f:
        json.dump(results_dict, f, indent=2)
    
    print(f"Performance results saved to {filename}")

@pytest.fixture(scope="session", autouse=True)
def collect_performance_results(request):
    """
    Fixture to collect and save performance test results.
    """
    results = {
        "timestamp": time.time(),
        "thresholds": PERFORMANCE_THRESHOLDS,
        "results": {}
    }
    
    yield results
    
    # Save results if any performance tests were run
    if results.get("results"):
        save_performance_results(results)
