"""
Utility for loading test data from JSON, CSV, or other formats.
"""
import json
import csv
import os
from typing import Dict, List, Any

def load_json_data(file_path: str) -> Dict[str, Any]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        Dict containing the JSON data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
        
    with open(file_path, 'r') as f:
        return json.load(f)

def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """
    Load data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        List of dictionaries, each representing a row in the CSV
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
        
    data = []
    with open(file_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            data.append(row)
    return data

def get_test_data_path(file_name: str) -> str:
    """
    Get the absolute path to a test data file.
    
    Args:
        file_name: Name of the test data file
    
    Returns:
        Absolute path to the test data file
    """
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the project root
    project_root = os.path.dirname(current_dir)
    
    # Construct the path to the test data file
    data_dir = os.path.join(project_root, "data")
    
    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    return os.path.join(data_dir, file_name)
