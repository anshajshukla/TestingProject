"""
Test file containing intentional failure cases to test error handling and reporting.
These tests are designed to fail in different ways to ensure the testing framework
can properly handle and report various failure scenarios.
"""
import pytest
import os
import numpy as np
import pandas as pd
import json
import time
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from utils.ml.data_generator import BankingDataGenerator
from utils.ml.test_prioritizer import TestPrioritizer

# Ensure test directories exist
@pytest.fixture(scope="module")
def setup_test_environment():
    """Create necessary directories for tests."""
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    return True

# Failure scenario 1: Invalid data input
def test_data_generator_with_invalid_input(setup_test_environment):
    """Test data generator with invalid inputs to ensure proper error handling."""
    # Test with invalid number of accounts (negative)
    with pytest.raises(ValueError):
        generator = BankingDataGenerator(num_accounts=-5)
        generator.generate_accounts()
    
    # Create valid generator for subsequent tests
    generator = BankingDataGenerator(num_accounts=2)
    
    # Test with empty accounts list
    with pytest.raises(ValueError):
        generator.generate_transactions([])
    
    # Test with invalid transaction parameters
    with pytest.raises(ValueError):
        generator.generate_transactions(generator.generate_accounts(), num_days=-10)

# Failure scenario 2: File system errors
def test_file_system_errors(setup_test_environment):
    """Test handling of file system errors when saving/loading data."""
    generator = BankingDataGenerator(num_accounts=2)
    
    # Try to save to a non-existent deep directory structure
    with pytest.raises(Exception):
        invalid_path = "X:/nonexistent/directory/structure/file.json"
        generator.save_test_data(invalid_path)
    
    # Try to read non-existent test history
    prioritizer = TestPrioritizer(history_file="nonexistent_file.csv")
    result = prioritizer.train()
    assert result is False, "Training should fail with non-existent history file"

# Failure scenario 3: Anomaly detection with corrupted data
def test_anomaly_detection_with_corrupted_data(setup_test_environment):
    """Test anomaly detection with corrupted or malformed data."""
    # Create a dataset with mixed types that will cause issues
    corrupted_data = np.array(['string', 1.0, None, 5.0, 'error']).reshape(-1, 1)
    
    # This should throw a TypeError when fitting the model
    with pytest.raises(TypeError):
        from sklearn.ensemble import IsolationForest
        model = IsolationForest(contamination=0.1)
        model.fit(corrupted_data)

# Failure scenario 4: Visualization failures
def test_visualization_failures(setup_test_environment):
    """Test visualization code with problematic data."""
    # Create an empty dataframe
    empty_df = pd.DataFrame()
    
    # Attempt to create a plot (should not crash but handle gracefully)
    plt.figure(figsize=(8, 6))
    try:
        # This should cause an error but not crash the test
        empty_df.plot(kind='scatter', x='non_existent_column', y='another_column')
        assert False, "Plot should have raised an error with empty dataframe"
    except Exception as e:
        # We expect an exception, so this is actually a successful test
        pass
    finally:
        plt.close()
    
    # Create a valid but minimal dataset to test boundary conditions
    minimal_df = pd.DataFrame({
        'single_value': [42]
    })
    
    # Plot should work with minimal data
    plt.figure(figsize=(8, 6))
    minimal_df.plot(kind='bar')
    plt.title("Minimal Dataset Test")
    plt.savefig("reports/minimal_data_test.png")
    plt.close()
    
    # Verify the image was created
    assert os.path.exists("reports/minimal_data_test.png"), "Plot file should exist"

# Failure scenario 5: Test prioritizer with edge cases
def test_prioritizer_edge_cases(setup_test_environment):
    """Test the test prioritizer with edge cases and boundary conditions."""
    # Create a sample test history with extreme values
    history = []
    
    # Add a few normal test results
    history.append({
        'test_name': 'normal_test',
        'module': 'normal',
        'result': 'pass',
        'duration': 1.0,
        'timestamp': pd.Timestamp.now().isoformat()
    })
    
    # Add a test with extremely long duration
    history.append({
        'test_name': 'slow_test',
        'module': 'performance',
        'result': 'fail',
        'duration': float('inf'),  # Infinite duration
        'timestamp': pd.Timestamp.now().isoformat()
    })
    
    # Add a test with zero duration
    history.append({
        'test_name': 'zero_test',
        'module': 'performance',
        'result': 'pass',
        'duration': 0.0,
        'timestamp': pd.Timestamp.now().isoformat()
    })
    
    # Save this to a test file
    history_df = pd.DataFrame(history)
    history_file = "data/edge_case_history.csv"
    history_df.to_csv(history_file, index=False)
    
    # Create prioritizer and attempt to train
    prioritizer = TestPrioritizer(history_file=history_file)
    result = prioritizer.train()
    
    # This should be handled gracefully despite the extreme values
    assert result, "Prioritizer should handle edge cases"
    
    # Test prioritization with an empty list
    empty_result = prioritizer.prioritize_tests([])
    assert isinstance(empty_result, list) and len(empty_result) == 0, "Should return empty list for empty input"
    
    # Test with strange test names
    strange_tests = [
        'test with spaces.py::test_function',
        '../../../../path/traversal/attempt.py::test_hack',
        'test_with_unicode_\u00fc\u00e4\u00f6.py::test_unicode',
        'test_empty_name.py::',
        '::test_no_filename'
    ]
    
    # This should handle all these cases without crashing
    strange_result = prioritizer.prioritize_tests(strange_tests)
    assert len(strange_result) == len(strange_tests), "Should handle unusual test names"

# Failure scenario 6: Test with threading and timing issues
def test_threading_and_timing_issues(setup_test_environment):
    """Test to verify handling of threading and timing issues."""
    # Perform multiple operations concurrently to test thread safety
    import threading
    
    # Create a shared generator
    generator = BankingDataGenerator(num_accounts=3)
    
    # Function to generate data from multiple threads
    def generate_data_threaded(thread_id):
        """Generate data from a thread."""
        # Each thread saves to its own file
        filename = f"data/thread_{thread_id}_data.json"
        try:
            test_data = generator.save_test_data(filename)
            assert len(test_data["transactions"]) > 0, "Should generate transactions"
        except Exception as e:
            pytest.fail(f"Thread {thread_id} failed: {str(e)}")
    
    # Create threads
    threads = []
    for i in range(3):  # Create 3 threads
        thread = threading.Thread(target=generate_data_threaded, args=(i,))
        threads.append(thread)
    
    # Start threads
    for thread in threads:
        thread.start()
    
    # Join threads
    for thread in threads:
        thread.join(timeout=10)  # Wait at most 10 seconds
    
    # Verify all threads completed
    for i in range(3):
        assert os.path.exists(f"data/thread_{i}_data.json"), f"Thread {i} should create a data file"

# Custom exception for testing
class CustomTestException(Exception):
    """Custom exception for testing error handling."""
    pass

# Failure scenario 7: Custom exception handling
def test_custom_exception_handling(setup_test_environment):
    """Test handling of custom exceptions."""
    with pytest.raises(CustomTestException):
        raise CustomTestException("This is a test exception")
    
    # Create a generator that will raise our custom exception
    class FailingGenerator(BankingDataGenerator):
        def generate_accounts(self):
            raise CustomTestException("Intentional failure in generate_accounts")
    
    # This should raise the custom exception
    with pytest.raises(CustomTestException):
        generator = FailingGenerator(num_accounts=1)
        generator.generate_accounts()

if __name__ == "__main__":
    pytest.main(["-v", __file__])
