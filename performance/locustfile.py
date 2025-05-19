"""
Performance testing for banking application using Locust.
"""
import json
import time
from locust import HttpUser, task, between
from utils.config import USERNAME, PASSWORD

class BankingUser(HttpUser):
    """
    Simulated banking application user for performance testing.
    """
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Login at the start of each simulated user session.
        """
        # API login
        response = self.client.post(
            "/api/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
            self.user_id = data.get("user_id")
        else:
            self.environment.runner.quit()
            raise Exception(f"Failed to login: {response.text}")
    
    @task(2)
    def view_dashboard(self):
        """
        Simulate viewing the dashboard (most frequent action).
        """
        self.client.get("/dashboard")
    
    @task(1)
    def view_accounts(self):
        """
        Simulate viewing account details.
        """
        response = self.client.get("/api/accounts")
        
        if response.status_code == 200:
            accounts = response.json().get("accounts", [])
            if accounts:
                # View details of the first account
                account_id = accounts[0]["id"]
                self.client.get(f"/accounts/{account_id}")
    
    @task(1)
    def view_transactions(self):
        """
        Simulate viewing transaction history.
        """
        self.client.get("/api/transactions")
    
    @task(0.5)
    def make_transfer(self):
        """
        Simulate making a fund transfer (less frequent action).
        """
        # Get accounts first
        response = self.client.get("/api/accounts")
        
        if response.status_code == 200:
            accounts = response.json().get("accounts", [])
            if len(accounts) >= 2:
                # Make transfer between first two accounts
                transfer_data = {
                    "from_account": accounts[0]["id"],
                    "to_account": accounts[1]["id"],
                    "amount": 100.00,
                    "description": f"Locust test transfer {time.time()}"
                }
                
                self.client.post(
                    "/api/transactions",
                    json=transfer_data
                )


class APIOnlyUser(HttpUser):
    """
    API-only user for testing backend performance without UI overhead.
    """
    wait_time = between(0.5, 3)
    
    def on_start(self):
        """
        Login at the start of each simulated API user session.
        """
        response = self.client.post(
            "/api/login",
            json={"username": USERNAME, "password": PASSWORD}
        )
        
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            self.environment.runner.quit()
            raise Exception(f"Failed to login: {response.text}")
    
    @task
    def get_accounts(self):
        """Get all accounts."""
        self.client.get("/api/accounts")
    
    @task
    def get_transactions(self):
        """Get transaction history."""
        self.client.get("/api/transactions")
    
    @task(0.3)
    def get_account_details(self):
        """Get details for a specific account."""
        response = self.client.get("/api/accounts")
        
        if response.status_code == 200:
            accounts = response.json().get("accounts", [])
            if accounts:
                account_id = accounts[0]["id"]
                self.client.get(f"/api/accounts/{account_id}")
