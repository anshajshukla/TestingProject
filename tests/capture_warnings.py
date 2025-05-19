"""
Script to capture warnings during test execution and log them to a file.
"""
import warnings
import sys
import os
import io
from contextlib import redirect_stderr

def main():
    # Create a file to store the warnings
    with io.StringIO() as buf, redirect_stderr(buf):
        # Ensure warnings are shown
        warnings.filterwarnings('always')
        
        # Run pytest
        os.system('python -m pytest tests/aiml/test_visualization.py -v')
        
        # Get the warnings output
        warnings_output = buf.getvalue()
    
    # Write the warnings to a file
    with open('warnings_log.txt', 'w') as f:
        f.write(warnings_output)
    
    print("Warnings captured and saved to warnings_log.txt")

if __name__ == "__main__":
    main()
