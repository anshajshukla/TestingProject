"""
Machine learning-powered test prioritization.
This utility helps prioritize which tests to run based on historical test failure data.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import time
import json
from datetime import datetime

class MLTestPrioritizer:
    """
    ML-powered test prioritization for banking test suite.
    Uses historical test execution data to predict which tests are likely to fail.
    """
    
    def __init__(self, history_file=None, model_file=None):
        """
        Initialize the test prioritizer.
        
        Args:
            history_file: Path to test execution history file
            model_file: Path to saved model file
        """
        self.history_file = history_file or "data/test_history.csv"
        self.model_file = model_file or "data/test_prioritizer_model.pkl"
        self.model = None
        self.features = None
        
        # Try to load existing model
        self._load_model()
    
    def _load_model(self):
        """
        Load the trained model if it exists.
        """
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.features = model_data['features']
                    print(f"Loaded existing model from {self.model_file}")
                    return True
            except Exception as e:
                print(f"Error loading model: {str(e)}")
        
        print("No existing model found or failed to load model")
        return False
    
    def _save_model(self):
        """
        Save the trained model to file.
        """
        if self.model and self.features:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
            
            model_data = {
                'model': self.model,
                'features': self.features,
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                with open(self.model_file, 'wb') as f:
                    pickle.dump(model_data, f)
                print(f"Model saved to {self.model_file}")
                return True
            except Exception as e:
                print(f"Error saving model: {str(e)}")
        
        return False
    
    def train(self, history_df=None):
        """
        Train the model on historical test execution data.
        
        Args:
            history_df: DataFrame with test execution history
                        If None, attempts to load from history_file
        
        Returns:
            bool: True if training was successful
        """
        # Load history data if not provided
        if history_df is None:
            if not os.path.exists(self.history_file):
                print(f"History file not found: {self.history_file}")
                return False
            
            try:
                history_df = pd.read_csv(self.history_file)
            except Exception as e:
                print(f"Error loading history data: {str(e)}")
                return False
        
        # Check if we have enough data to train
        if len(history_df) < 10:
            print("Not enough data to train the model (minimum 10 records needed)")
            return False
        
        # Prepare features
        required_columns = ['test_name', 'module', 'duration', 'result']
        if not all(col in history_df.columns for col in required_columns):
            print(f"Missing required columns in history data. Required: {required_columns}")
            return False
        
        # Engineer features
        history_df['hour_of_day'] = pd.to_datetime(history_df['timestamp']).dt.hour if 'timestamp' in history_df.columns else 12
        history_df['day_of_week'] = pd.to_datetime(history_df['timestamp']).dt.dayofweek if 'timestamp' in history_df.columns else 0
        
        # One-hot encode categorical features
        modules = pd.get_dummies(history_df['module'], prefix='module')
        history_df = pd.concat([history_df, modules], axis=1)
        
        # Add failure rate for each test_name
        test_failure_rates = history_df.groupby('test_name')['result'].apply(
            lambda x: (x == 'fail').mean()
        ).reset_index()
        test_failure_rates.columns = ['test_name', 'failure_rate']
        history_df = pd.merge(history_df, test_failure_rates, on='test_name', how='left')
        
        # Define features and target
        feature_cols = [col for col in history_df.columns if col.startswith('module_')] + ['duration', 'hour_of_day', 'day_of_week', 'failure_rate']
        self.features = feature_cols
        
        # Extract feature matrix with explicit feature names
        X = history_df[feature_cols].copy()
        
        # Convert target to 1 for fail, 0 for pass
        y = (history_df['result'] == 'fail').astype(int)
        
        # Train model with explicit feature_names parameter to avoid warnings
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)
        self.model = model
        
        # Save model
        self._save_model()
        
        print(f"Model trained successfully with {len(feature_cols)} features")
        return True
    
    def prioritize_tests(self, tests_to_run, test_metadata=None):
        """
        Prioritize the tests based on failure probability.
        
        Args:
            tests_to_run: List of test names to prioritize
            test_metadata: Optional dict with metadata for each test
        
        Returns:
            list: Tests sorted by failure probability (highest first)
        """
        if not self.model or not self.features:
            print("No trained model available. Running tests in original order.")
            return tests_to_run
        
        if not test_metadata:
            # Try to derive basic metadata
            test_metadata = {}
            for test in tests_to_run:
                parts = test.split('::')
                if len(parts) >= 2:
                    module = parts[0]
                    test_name = parts[-1]
                else:
                    module = 'unknown'
                    test_name = test
                
                test_metadata[test] = {
                    'test_name': test_name,
                    'module': module,
                    'duration': 1.0,  # Default duration
                    'failure_rate': 0.1  # Default failure rate
                }
        
        # Prepare features for prediction
        test_features = []
        for test in tests_to_run:
            meta = test_metadata.get(test, {})
            
            # Create feature row
            feature_row = {
                'duration': meta.get('duration', 1.0),
                'hour_of_day': datetime.now().hour,
                'day_of_week': datetime.now().weekday(),
                'failure_rate': meta.get('failure_rate', 0.1)
            }
            
            # Add module one-hot encoding
            module = meta.get('module', 'unknown')
            for feature in self.features:
                if feature.startswith('module_'):
                    module_name = feature[len('module_'):]
                    feature_row[feature] = 1 if module == module_name else 0
            
            test_features.append((test, feature_row))
        
        # Make predictions
        results = []
        for test, features in test_features:
            # Prepare feature vector as a DataFrame with correct column names
            feature_dict = {feature: features.get(feature, 0) for feature in self.features}
            feature_df = pd.DataFrame([feature_dict])
            
            # Predict failure probability using DataFrame with proper column names
            try:
                failure_prob = self.model.predict_proba(feature_df)[0][1]
            except Exception:
                # Fallback in case of any issues with prediction
                failure_prob = 0.5  # Default to middle probability
                
            results.append((test, failure_prob))
        
        # Sort by failure probability (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return sorted tests
        return [test for test, _ in results]
    
    def record_test_results(self, test_results):
        """
        Record test execution results to history file.
        
        Args:
            test_results: List of dictionaries with test results
                        Each dict should have: test_name, module, duration, result
        
        Returns:
            bool: True if recording was successful
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        
        # Read existing history if available
        if os.path.exists(self.history_file):
            try:
                history_df = pd.read_csv(self.history_file)
            except Exception:
                history_df = pd.DataFrame()
        else:
            history_df = pd.DataFrame()
        
        # Convert test results to DataFrame
        for result in test_results:
            if 'timestamp' not in result:
                result['timestamp'] = datetime.now().isoformat()
        
        results_df = pd.DataFrame(test_results)
        
        # Append new results
        history_df = pd.concat([history_df, results_df], ignore_index=True)
        
        # Save updated history
        try:
            history_df.to_csv(self.history_file, index=False)
            print(f"Test results recorded in {self.history_file}")
            return True
        except Exception as e:
            print(f"Error recording test results: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    # Create sample test history if it doesn't exist
    if not os.path.exists("data/test_history.csv"):
        os.makedirs("data", exist_ok=True)
        
        # Generate sample history
        modules = ['ui', 'api', 'security', 'smoke']
        test_names = [
            'test_login', 'test_logout', 'test_transfer', 
            'test_account_details', 'test_transaction_history'
        ]
        
        history = []
        for i in range(100):
            module = np.random.choice(modules)
            test_name = np.random.choice(test_names)
            result = np.random.choice(['pass', 'fail'], p=[0.8, 0.2])
            duration = np.random.uniform(0.5, 5.0)
            timestamp = datetime.now().isoformat()
            
            history.append({
                'test_name': test_name,
                'module': module,
                'result': result,
                'duration': duration,
                'timestamp': timestamp
            })

        history_df = pd.DataFrame(history)
        history_df.to_csv("data/test_history.csv", index=False)
        print("Created sample test history")

    # Create a test prioritizer
    prioritizer = MLTestPrioritizer()
    prioritizer.train()

    tests_to_run = [
        'tests/ui/test_login.py::test_valid_login',
        'tests/ui/test_login.py::test_invalid_login',
        'tests/api/test_auth.py::test_login_success',
        'tests/api/test_transactions.py::test_get_transactions',
        'tests/smoke/test_health.py::test_ui_health'
    ]
    
    prioritized_tests = prioritizer.prioritize_tests(tests_to_run)
    print("\nPrioritized tests:")
    for i, test in enumerate(prioritized_tests):
        print(f"{i+1}. {test}")
