"""
Script to explicitly capture and display all warnings that occur during tests.
"""
import warnings
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Capture all warnings
warnings.filterwarnings('always')

# Create a custom warning handler
def warning_handler(message, category, filename, lineno, file=None, line=None):
    print(f"\n{'='*80}")
    print(f"WARNING: {category.__name__}")
    print(f"File: {filename}, Line: {lineno}")
    print(f"Message: {message}")
    print(f"{'='*80}\n")

# Set custom handler
warnings.showwarning = warning_handler

# Import the test module to execute it with our warning handler
from test_visualization import test_basic_matplotlib_rendering, test_seaborn_visualization, test_transaction_visualizations

# Run the tests manually
print("Running test_basic_matplotlib_rendering...")
test_basic_matplotlib_rendering(None)

print("\nRunning test_seaborn_visualization...")
test_seaborn_visualization(None)

print("\nRunning test_transaction_visualizations...")
setup_result = {}  # Mock setup result
test_transaction_visualizations(setup_result)

print("\nAll tests completed. Any warnings should be displayed above.")
