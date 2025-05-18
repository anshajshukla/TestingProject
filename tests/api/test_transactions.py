"""
API tests for transaction endpoints.
"""
import pytest
import uuid
from datetime import datetime
from utils.config import API_URL

def test_get_transactions(authenticated_session):
    """
    Test retrieving transaction history.
    """
    response = authenticated_session.get(f"{API_URL}/transactions")
    
    assert response.status_code == 200, f"Failed to get transactions. Status code: {response.status_code}"
    data = response.json()
    assert "transactions" in data, "Response doesn't contain transactions field"
    assert isinstance(data["transactions"], list), "Transactions field is not a list"

def test_get_transaction_details(authenticated_session):
    """
    Test retrieving details for a specific transaction.
    """
    # First get all transactions
    response = authenticated_session.get(f"{API_URL}/transactions")
    assert response.status_code == 200
    
    transactions = response.json().get("transactions", [])
    if not transactions:
        pytest.skip("No transactions available to test details")
    
    # Get details for the first transaction
    transaction_id = transactions[0]["id"]
    response = authenticated_session.get(f"{API_URL}/transactions/{transaction_id}")
    
    assert response.status_code == 200, f"Failed to get transaction details. Status code: {response.status_code}"
    data = response.json()
    assert "id" in data, "Transaction details don't contain id field"
    assert data["id"] == transaction_id, f"Transaction ID mismatch. Expected: {transaction_id}, Got: {data['id']}"

def test_create_transaction(authenticated_session):
    """
    Test creating a new transaction.
    """
    transaction_data = {
        "from_account": "12345678",
        "to_account": "87654321",
        "amount": 100.00,
        "description": f"Test transaction {datetime.now().isoformat()}"
    }
    
    response = authenticated_session.post(
        f"{API_URL}/transactions",
        json=transaction_data
    )
    
    assert response.status_code == 201, f"Failed to create transaction. Status code: {response.status_code}"
    data = response.json()
    assert "id" in data, "Response doesn't contain transaction id"
    assert "status" in data, "Response doesn't contain status field"
    assert data["status"] == "completed" or data["status"] == "pending", f"Unexpected status: {data['status']}"
    
    # Verify the transaction was created by getting its details
    transaction_id = data["id"]
    response = authenticated_session.get(f"{API_URL}/transactions/{transaction_id}")
    assert response.status_code == 200

def test_invalid_transaction_amount(authenticated_session):
    """
    Test that negative or zero amounts are rejected.
    """
    # Test with negative amount
    transaction_data = {
        "from_account": "12345678",
        "to_account": "87654321",
        "amount": -100.00,
        "description": "Negative amount test"
    }
    
    response = authenticated_session.post(
        f"{API_URL}/transactions",
        json=transaction_data
    )
    
    assert response.status_code == 400, f"Expected 400 status code for negative amount, got: {response.status_code}"
    
    # Test with zero amount
    transaction_data["amount"] = 0
    
    response = authenticated_session.post(
        f"{API_URL}/transactions",
        json=transaction_data
    )
    
    assert response.status_code == 400, f"Expected 400 status code for zero amount, got: {response.status_code}"

def test_insufficient_funds(authenticated_session):
    """
    Test transaction with insufficient funds is rejected.
    """
    # Assuming a very large amount that exceeds available balance
    transaction_data = {
        "from_account": "12345678",
        "to_account": "87654321",
        "amount": 1000000.00,
        "description": "Insufficient funds test"
    }
    
    response = authenticated_session.post(
        f"{API_URL}/transactions",
        json=transaction_data
    )
    
    assert response.status_code == 400, f"Expected 400 status code for insufficient funds, got: {response.status_code}"
    data = response.json()
    assert "error" in data, "Error message not found in response"
    assert "insufficient funds" in data["error"].lower(), f"Unexpected error message: {data['error']}"
