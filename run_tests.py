#!/usr/bin/env python
"""
Test runner script for the Banking/Fintech Testing Framework.
This script provides a convenient command-line interface for running different test suites.
"""
import argparse
import os
import subprocess
import sys
import time

def main():
    """Parse arguments and run the specified tests."""
    parser = argparse.ArgumentParser(description="Banking Tests Runner")
    
    # Add command-line arguments
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--ui", action="store_true", help="Run UI tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--report", action="store_true", help="Generate Allure report")
    parser.add_argument("--serve-report", action="store_true", help="Serve the Allure report")
    parser.add_argument("--parallel", type=int, default=0, help="Number of parallel processes (0 for sequential)")
    
    args = parser.parse_args()
    
    # If no test type is specified, show help
    if not any([args.smoke, args.api, args.ui, args.security, args.all, args.report, args.serve_report]):
        parser.print_help()
        return
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Set up common pytest arguments
    pytest_args = []
    
    # Add Allure report directory if requested
    if args.report:
        pytest_args.extend(["--alluredir", "reports/allure"])
    
    # Add parallel execution if requested
    if args.parallel > 0:
        pytest_args.extend(["-n", str(args.parallel)])
    
    # Determine which tests to run
    test_dirs = []
    
    if args.all:
        test_dirs = ["tests"]
    else:
        if args.smoke:
            test_dirs.append("tests/smoke")
        if args.api:
            test_dirs.append("tests/api")
        if args.ui:
            test_dirs.append("tests/ui")
        if args.security:
            test_dirs.append("tests/security")
    
    # Run the tests
    if test_dirs:
        cmd = ["pytest"] + pytest_args + test_dirs
        print(f"Running command: {' '.join(cmd)}")
        start_time = time.time()
        result = subprocess.run(cmd)
        end_time = time.time()
        
        print(f"\nTests completed in {end_time - start_time:.2f} seconds with exit code {result.returncode}")
    
    # Serve the Allure report if requested
    if args.serve_report:
        subprocess.run(["allure", "serve", "reports/allure"])

if __name__ == "__main__":
    main()
