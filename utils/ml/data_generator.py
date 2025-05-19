"""
ML-powered data generator for realistic banking test data.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import json
import os

class BankingDataGenerator:
    """
    Generator for realistic banking transaction data using machine learning techniques.
    """
    
    def __init__(self, num_accounts=5, seed=42):
        """
        Initialize the data generator with configuration.
        
        Args:
            num_accounts: Number of accounts to generate
            seed: Random seed for reproducibility
            
        Raises:
            ValueError: If num_accounts is less than 1
        """
        if num_accounts < 1:
            raise ValueError("Number of accounts must be at least 1")
            
        self.num_accounts = num_accounts
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
        # Define transaction categories and their probability weights
        self.categories = {
            'Groceries': 0.25,
            'Shopping': 0.15,
            'Dining': 0.15,
            'Entertainment': 0.1,
            'Utilities': 0.08,
            'Transport': 0.12,
            'Healthcare': 0.05, 
            'Education': 0.03,
            'Travel': 0.05,
            'Miscellaneous': 0.02
        }
        
        # Define spending patterns by hour of day (24-hour format)
        self.hourly_patterns = {
            0: 0.01, 1: 0.01, 2: 0.01, 3: 0.01, 4: 0.01, 5: 0.02,
            6: 0.03, 7: 0.05, 8: 0.07, 9: 0.08, 10: 0.07, 11: 0.08,
            12: 0.1, 13: 0.09, 14: 0.07, 15: 0.06, 16: 0.07, 17: 0.08,
            18: 0.09, 19: 0.07, 20: 0.06, 21: 0.05, 22: 0.03, 23: 0.02
        }
        
        # Define typical transaction amount ranges by category
        self.amount_ranges = {
            'Groceries': (10, 200),
            'Shopping': (15, 500),
            'Dining': (15, 150),
            'Entertainment': (10, 100),
            'Utilities': (30, 300),
            'Transport': (5, 100),
            'Healthcare': (20, 500),
            'Education': (50, 1000),
            'Travel': (100, 2000),
            'Miscellaneous': (5, 200)
        }
    
    def generate_accounts(self):
        """
        Generate a set of bank accounts with initial balances.
        
        Returns:
            list: List of account dictionaries
        """
        accounts = []
        account_types = ['Checking', 'Savings', 'Credit Card']
        
        for i in range(self.num_accounts):
            account_type = random.choice(account_types)
            balance = round(np.random.lognormal(mean=8, sigma=1), 2)
            
            # Credit cards have negative balances typically
            if account_type == 'Credit Card':
                balance = -round(np.random.lognormal(mean=6, sigma=1), 2)
                credit_limit = abs(balance) * 2
            
            account = {
                'account_id': f"{random.randint(10000000, 99999999)}",
                'account_type': account_type,
                'balance': balance,
                'currency': 'USD',
                'owner_id': f"user{random.randint(100, 999)}"
            }
            
            if account_type == 'Credit Card':
                account['credit_limit'] = credit_limit
            
            accounts.append(account)
        
        return accounts
    
    def generate_transactions(self, accounts, num_days=30, transactions_per_day=5):
        """
        Generate realistic banking transactions for the given accounts.
        
        Args:
            accounts: List of account dictionaries
            num_days: Number of days of history to generate
            transactions_per_day: Average number of transactions per day
        
        Returns:
            list: List of transaction dictionaries
            
        Raises:
            ValueError: If accounts list is empty or parameters are invalid
        """
        if not accounts:
            raise ValueError("Accounts list cannot be empty")
            
        if num_days < 1:
            raise ValueError("Number of days must be at least 1")
            
        if transactions_per_day < 0:
            raise ValueError("Transactions per day cannot be negative")
            
        transactions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=num_days)
        
        account_ids = [a['account_id'] for a in accounts]
        
        # For each day in the range
        current_date = start_date
        while current_date <= end_date:
            # Randomize number of transactions for this day
            daily_count = max(1, int(np.random.normal(transactions_per_day, 2)))
            
            for _ in range(daily_count):
                # Get random hour based on hourly pattern weights
                hour = random.choices(
                    list(self.hourly_patterns.keys()),
                    weights=list(self.hourly_patterns.values())
                )[0]
                
                # Create transaction timestamp
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                timestamp = current_date.replace(hour=hour, minute=minute, second=second)
                
                # Select category based on weights
                category = random.choices(
                    list(self.categories.keys()),
                    weights=list(self.categories.values())
                )[0]
                
                # Generate amount based on category range
                min_amount, max_amount = self.amount_ranges[category]
                
                # Use log-normal distribution for more realistic amounts
                mu = np.log((min_amount + max_amount) / 2)
                sigma = 0.5
                amount = round(np.random.lognormal(mu, sigma), 2)
                
                # Clamp to range
                amount = max(min_amount, min(amount, max_amount))
                
                # Select random from and to accounts
                from_account = random.choice(account_ids)
                to_account = random.choice([a for a in account_ids if a != from_account])
                
                # Create transaction
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': from_account,
                    'to_account': to_account,
                    'amount': amount,
                    'category': category,
                    'timestamp': timestamp.isoformat(),
                    'status': 'completed',
                    'description': f"{category} - {self._generate_description(category)}"
                }
                
                transactions.append(transaction)
            
            # Move to next day
            current_date += timedelta(days=1)
        
        # Sort by timestamp
        transactions.sort(key=lambda x: x['timestamp'])
        return transactions
    
    def _generate_description(self, category):
        """Generate a realistic description based on category."""
        descriptions = {
            'Groceries': ['Supermarket', 'Food Store', 'Grocery Delivery', 'Local Market'],
            'Shopping': ['Online Purchase', 'Department Store', 'Electronics', 'Clothing Store'],
            'Dining': ['Restaurant', 'Fast Food', 'Coffee Shop', 'Food Delivery'],
            'Entertainment': ['Movies', 'Streaming Service', 'Concert', 'Game Purchase'],
            'Utilities': ['Electricity Bill', 'Water Bill', 'Internet Service', 'Phone Bill'],
            'Transport': ['Ride Share', 'Fuel', 'Parking', 'Public Transit'],
            'Healthcare': ['Pharmacy', 'Doctor Visit', 'Medical Test', 'Insurance'],
            'Education': ['Tuition', 'Books', 'Online Course', 'School Supplies'],
            'Travel': ['Flight Ticket', 'Hotel Booking', 'Vacation Package', 'Car Rental'],
            'Miscellaneous': ['Subscription', 'Membership Fee', 'Service Charge', 'Donation']
        }
        
        return random.choice(descriptions.get(category, ['Payment']))
    
    def generate_anomalous_transactions(self, accounts, normal_transactions, num_anomalies=5):
        """
        Generate anomalous banking transactions for testing fraud detection.
        
        Args:
            accounts: List of account dictionaries
            normal_transactions: List of normal transactions for reference
            num_anomalies: Number of anomalous transactions to generate
        
        Returns:
            list: List of anomalous transaction dictionaries
        """
        anomalies = []
        account_ids = [a['account_id'] for a in accounts]
        
        for _ in range(num_anomalies):
            # Randomly choose anomaly type
            anomaly_type = random.choice([
                'large_amount', 
                'unusual_time', 
                'unusual_location',
                'multiple_quick_transactions',
                'unusual_category'
            ])
            
            if anomaly_type == 'large_amount':
                # Transaction with unusually large amount
                category = random.choice(list(self.categories.keys()))
                _, max_amount = self.amount_ranges[category]
                amount = max_amount * random.uniform(5, 20)
                
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': random.choice(account_ids),
                    'to_account': f"{random.randint(10000000, 99999999)}",  # Unknown account
                    'amount': round(amount, 2),
                    'category': category,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'completed',
                    'description': f"{category} - Anomalous large payment",
                    'is_anomaly': True,
                    'anomaly_type': 'large_amount'
                }
                
            elif anomaly_type == 'unusual_time':
                # Transaction at unusual hour (middle of night)
                category = random.choice(list(self.categories.keys()))
                min_amount, max_amount = self.amount_ranges[category]
                amount = random.uniform(min_amount, max_amount)
                
                # Create timestamp at unusual hour (2-4 AM)
                hour = random.randint(2, 4)
                minute = random.randint(0, 59)
                timestamp = datetime.now().replace(hour=hour, minute=minute)
                
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': random.choice(account_ids),
                    'to_account': random.choice(account_ids),
                    'amount': round(amount, 2),
                    'category': category,
                    'timestamp': timestamp.isoformat(),
                    'status': 'completed',
                    'description': f"{category} - Late night transaction",
                    'is_anomaly': True,
                    'anomaly_type': 'unusual_time'
                }
                
            elif anomaly_type == 'unusual_location':
                # Transaction from unusual location
                category = random.choice(['Shopping', 'Dining', 'Entertainment'])
                min_amount, max_amount = self.amount_ranges[category]
                amount = random.uniform(min_amount, max_amount)
                
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': random.choice(account_ids),
                    'to_account': f"{random.randint(10000000, 99999999)}",  # Unknown account
                    'amount': round(amount, 2),
                    'category': category,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'completed',
                    'description': f"{category} - Foreign country transaction",
                    'location': random.choice(['Cambodia', 'Nigeria', 'Belarus', 'Kazakhstan']),
                    'is_anomaly': True,
                    'anomaly_type': 'unusual_location'
                }
                
            elif anomaly_type == 'multiple_quick_transactions':
                # Multiple transactions in quick succession
                category = random.choice(['Shopping', 'ATM Withdrawal'])
                min_amount, max_amount = self.amount_ranges.get(category, (50, 200))
                
                # Base transaction
                base_time = datetime.now()
                account = random.choice(account_ids)
                
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': account,
                    'to_account': f"{random.randint(10000000, 99999999)}",
                    'amount': round(random.uniform(min_amount, max_amount), 2),
                    'category': category,
                    'timestamp': base_time.isoformat(),
                    'status': 'completed',
                    'description': f"{category} - Quick succession transaction 1/3",
                    'is_anomaly': True,
                    'anomaly_type': 'multiple_quick_transactions',
                    'related_transactions': []  # Will be filled with IDs
                }
                
                # Add two more transactions in quick succession
                for i in range(2):
                    related_id = f"T{random.randint(1000000, 9999999)}"
                    transaction['related_transactions'].append(related_id)
                    
                    related_transaction = {
                        'transaction_id': related_id,
                        'from_account': account,
                        'to_account': f"{random.randint(10000000, 99999999)}",
                        'amount': round(random.uniform(min_amount, max_amount), 2),
                        'category': category,
                        'timestamp': (base_time + timedelta(minutes=i+1)).isoformat(),
                        'status': 'completed',
                        'description': f"{category} - Quick succession transaction {i+2}/3",
                        'is_anomaly': True,
                        'anomaly_type': 'multiple_quick_transactions',
                        'primary_transaction_id': transaction['transaction_id']
                    }
                    anomalies.append(related_transaction)
                
            elif anomaly_type == 'unusual_category':
                # Transaction in category user never uses
                # Find unused categories
                used_categories = set([t['category'] for t in normal_transactions])
                unused_categories = set(self.categories.keys()) - used_categories
                
                if unused_categories:
                    category = random.choice(list(unused_categories))
                else:
                    # If all categories used, pick least used
                    category_counts = {}
                    for t in normal_transactions:
                        cat = t.get('category')
                        if cat:
                            category_counts[cat] = category_counts.get(cat, 0) + 1
                    
                    least_used = min(category_counts.items(), key=lambda x: x[1])[0]
                    category = least_used
                
                min_amount, max_amount = self.amount_ranges.get(category, (50, 200))
                amount = random.uniform(min_amount, max_amount)
                
                transaction = {
                    'transaction_id': f"T{random.randint(1000000, 9999999)}",
                    'from_account': random.choice(account_ids),
                    'to_account': f"{random.randint(10000000, 99999999)}",
                    'amount': round(amount, 2),
                    'category': category,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'completed',
                    'description': f"{category} - Unusual category for this user",
                    'is_anomaly': True,
                    'anomaly_type': 'unusual_category'
                }
            
            anomalies.append(transaction)
        
        return anomalies
    
    def save_test_data(self, filepath):
        """
        Generate and save complete test data to a file.
        
        Args:
            filepath: Path to save the JSON data
        
        Returns:
            dict: Generated test data
            
        Raises:
            OSError: If the file cannot be created or written to
            ValueError: If filepath is invalid
        """
        if not filepath:
            raise ValueError("Filepath cannot be empty")
            
        try:
            # Generate accounts
            accounts = self.generate_accounts()
            
            # Generate normal transactions
            transactions = self.generate_transactions(accounts)
            
            # Generate anomalous transactions
            anomalies = self.generate_anomalous_transactions(accounts, transactions)
            
            # Combine all transactions
            all_transactions = transactions + anomalies
            
            # Sort by timestamp
            all_transactions.sort(key=lambda x: x['timestamp'])
            
            # Create test data structure
            test_data = {
                'accounts': accounts,
                'transactions': all_transactions,
                'metadata': {
                    'generated_on': datetime.now().isoformat(),
                    'num_accounts': len(accounts),
                    'num_transactions': len(all_transactions),
                    'num_anomalies': len(anomalies)
                }
            }
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(test_data, f, indent=2)
            
            return test_data
            
        except OSError as e:
            raise OSError(f"Could not save data to {filepath}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating or saving test data: {str(e)}")

# Usage example
if __name__ == "__main__":
    generator = BankingDataGenerator(num_accounts=5)
    generator.save_test_data('data/generated_banking_data.json')
