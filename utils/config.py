"""
Configuration utilities for the banking tests project.
Loads environment variables from .env file.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs for the application
BASE_URL = os.getenv("BASE_URL", "https://demo-bank.com")
API_URL = os.getenv("API_URL", "https://api.demo-bank.com")

# Test user credentials
USERNAME = os.getenv("USERNAME", "testuser")
PASSWORD = os.getenv("PASSWORD", "Test@123")

# Browser configuration
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"

# Timeouts
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
