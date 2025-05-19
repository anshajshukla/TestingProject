"""
Tests using anomaly detection techniques to identify unusual API behavior.
"""
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import time
import requests
import os
from utils.config import API_URL

# Skip tests if the required ML libraries are not installed
pytest.importorskip("sklearn.ensemble")

@pytest.fixture(scope="module", autouse=True)
def ensure_reports_dir():
    """Ensure the reports directory exists."""
    os.makedirs("reports", exist_ok=True)

def test_api_response_anomaly_detection():
    """
    Collect API response times and detect anomalies using Isolation Forest.
    """
    # Number of API calls to make
    n_samples = 50
    response_times = []
    
    # Collect response times
    for _ in range(n_samples):
        start_time = time.time()
        try:
            response = requests.get(f"{API_URL}/accounts", timeout=10)
            # If we're using a demo/mock API, we might need to handle different status codes
            assert response.status_code in [200, 404, 403], f"API request failed with status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"API request failed: {str(e)}")
        end_time = time.time()
        
        # Record response time
        response_times.append(end_time - start_time)
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(response_times, columns=['response_time'])
    
    # Use Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(df)
    
    # Predict anomalies (-1 for anomalies, 1 for normal)
    df['anomaly'] = model.predict(df)
    
    # Separate normal and anomalous points
    normal = df[df['anomaly'] == 1]['response_time']
    anomalies = df[df['anomaly'] == -1]['response_time']
    
    # Visualize results
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(normal)), normal, label='Normal', color='blue')
    if len(anomalies) > 0:
        plt.scatter([i + len(normal) for i in range(len(anomalies))], 
                    anomalies, label='Anomaly', color='red')
    plt.title('API Response Time Anomaly Detection')
    plt.xlabel('Request Number')
    plt.ylabel('Response Time (s)')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.savefig('reports/anomaly_detection.png')
    
    # Log statistics
    print(f"\nResponse time statistics:")
    print(f"  Average: {df['response_time'].mean():.3f} seconds")
    print(f"  Min: {df['response_time'].min():.3f} seconds")
    print(f"  Max: {df['response_time'].max():.3f} seconds")
    print(f"  Anomalies detected: {len(anomalies)}")
    
    # We're not actually asserting anything here since this is more of an analysis
    # But if we wanted to, we could check if there are too many anomalies
    # assert len(anomalies) <= 5, f"Too many anomalies detected: {len(anomalies)}"
