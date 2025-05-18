"""
Dashboard application for Banking Test Framework ML components.
This dashboard visualizes the ML testing capabilities including:
- Anomaly detection in API responses
- ML-powered test prioritization
- Realistic test data generation
"""
from flask import Flask, render_template, jsonify, request
import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Configure seaborn with better defaults for web display
import seaborn as sns

# Use the new seaborn defaults that don't cause warnings
sns.set_theme(style="whitegrid")
sns.set_context("talk")

# Explicitly set boxplot settings to avoid deprecation warnings
sns.set_style("whitegrid")

# Set Matplotlib's boxplot parameters directly to avoid seaborn warnings
from matplotlib.pyplot import boxplot as mpl_boxplot
plt.rcParams['boxplot.boxprops.linewidth'] = 1.5
plt.rcParams['boxplot.whiskerprops.linewidth'] = 1.5
plt.rcParams['boxplot.capprops.linewidth'] = 1.5
plt.rcParams['boxplot.medianprops.linewidth'] = 1.5
plt.rcParams['boxplot.flierprops.markersize'] = 6

# Configure matplotlib for better web display
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
from datetime import datetime, timedelta
import io
import base64
from utils.ml.data_generator import BankingDataGenerator
from utils.ml.test_prioritizer import TestPrioritizer
import pickle

app = Flask(__name__)

# Set paths - ensure absolute paths are used
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')

# Add the root directory to Python path to ensure imports work correctly
import sys
sys.path.insert(0, ROOT_DIR)

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/generate-data', methods=['POST'])
def generate_data():
    """Generate banking test data using the ML-powered generator."""
    try:
        num_accounts = int(request.form.get('num_accounts', 5))
        transactions_per_day = int(request.form.get('transactions_per_day', 5))
        num_days = int(request.form.get('num_days', 30))
        
        print(f"Generating data with {num_accounts} accounts, {transactions_per_day} transactions/day for {num_days} days")
        
        # Ensure directories exist
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        # Create generator and generate data
        generator = BankingDataGenerator(num_accounts=num_accounts)
        
        # Save data to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"banking_data_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        print(f"Saving data to {filepath}")
        
        # Generate and save the data
        test_data = generator.save_test_data(filepath)
        
        # Create visualizations
        visualizations = create_data_visualizations(test_data)
        
        # Calculate statistics
        num_accounts = len(test_data['accounts'])
        num_transactions = len(test_data['transactions'])
        num_anomalies = len([t for t in test_data['transactions'] if t.get('is_anomaly', False)])
        
        # Calculate total and average transaction amounts
        if num_transactions > 0:
            total_value = sum(t['amount'] for t in test_data['transactions'])
            avg_transaction = total_value / num_transactions
        else:
            total_value = 0
            avg_transaction = 0
            
        # Get unique categories
        categories = list(set(t['category'] for t in test_data['transactions'] if 'category' in t))
        
        return jsonify({
            'status': 'success',
            'message': f'Generated {num_transactions} transactions for {num_accounts} accounts',
            'filename': filename,
            'visualizations': visualizations,
            'stats': {
                'num_accounts': num_accounts,
                'num_transactions': num_transactions,
                'num_anomalies': num_anomalies,
                'total_value': total_value,
                'avg_transaction': avg_transaction,
                'categories': categories
            }
        })
    except Exception as e:
        import traceback
        print(f"Error generating data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f'Error generating data: {str(e)}'
        }), 500

@app.route('/api/prioritize-tests', methods=['POST'])
def prioritize_tests():
    """Prioritize tests using the ML-powered test prioritizer."""
    # Get list of tests to prioritize
    tests = request.form.get('tests', '').split('\n')
    tests = [t.strip() for t in tests if t.strip()]
    
    if not tests:
        return jsonify({
            'status': 'error',
            'message': 'No tests provided'
        })
    
    # Create or use test history
    history_file = os.path.join(DATA_DIR, 'test_history.csv')
    
    # If no history exists, create sample history
    if not os.path.exists(history_file):
        create_sample_test_history(history_file, tests)
    
    # Create prioritizer and prioritize tests
    prioritizer = TestPrioritizer(history_file=history_file)
    
    # Train if not already trained
    prioritizer.train()
    
    # Prioritize tests
    prioritized_tests = prioritizer.prioritize_tests(tests)
    
    # Generate visualization of test failure rates
    failure_rate_img = generate_test_failure_rates(history_file, tests)
    
    return jsonify({
        'status': 'success',
        'message': f'Prioritized {len(tests)} tests',
        'prioritized_tests': prioritized_tests,
        'visualization': failure_rate_img
    })

@app.route('/api/anomaly-detection', methods=['POST'])
def detect_anomalies():
    """Detect anomalies in API response times or transaction data."""
    data_type = request.form.get('data_type', 'response_times')
    data_file = request.form.get('data_file', '')
    
    if data_type == 'response_times':
        # Generate sample response times if no file provided
        if not data_file or not os.path.exists(os.path.join(DATA_DIR, data_file)):
            response_times = generate_sample_response_times()
        else:
            with open(os.path.join(DATA_DIR, data_file), 'r') as f:
                data = json.load(f)
                response_times = data.get('response_times', [])
        
        # Detect anomalies
        anomalies, visualization = detect_response_time_anomalies(response_times)
        
        return jsonify({
            'status': 'success',
            'message': f'Detected {len(anomalies)} anomalies in {len(response_times)} response times',
            'anomalies': anomalies,
            'visualization': visualization
        })
    
    elif data_type == 'transactions':
        # Use a generated banking data file if no file provided
        if not data_file or not os.path.exists(os.path.join(DATA_DIR, data_file)):
            # Generate new data
            generator = BankingDataGenerator(num_accounts=3)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"banking_data_{timestamp}.json"
            filepath = os.path.join(DATA_DIR, filename)
            test_data = generator.save_test_data(filepath)
            transactions = test_data['transactions']
        else:
            # Load existing data
            with open(os.path.join(DATA_DIR, data_file), 'r') as f:
                test_data = json.load(f)
                transactions = test_data.get('transactions', [])
        
        # Detect anomalies in transaction amounts
        anomalies, visualization = detect_transaction_anomalies(transactions)
        
        return jsonify({
            'status': 'success',
            'message': f'Detected {len(anomalies)} anomalies in {len(transactions)} transactions',
            'anomalies': anomalies,
            'visualization': visualization
        })
    
    return jsonify({
        'status': 'error',
        'message': f'Unsupported data type: {data_type}'
    })

@app.route('/api/list-data-files', methods=['GET'])
def list_data_files():
    """List available data files in the data directory."""
    data_files = []
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') or filename.endswith('.csv'):
            filepath = os.path.join(DATA_DIR, filename)
            file_info = {
                'filename': filename,
                'size': os.path.getsize(filepath),
                'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            }
            data_files.append(file_info)
    
    return jsonify({
        'status': 'success',
        'data_files': data_files
    })

def create_data_visualizations(test_data):
    """Create visualizations for the generated banking data."""
    visualizations = {}
    
    try:
        # Transaction amounts by category
        plt.figure(figsize=(10, 6))
        transactions_df = pd.DataFrame(test_data['transactions'])
        
        # Ensure all required columns exist
        required_columns = ['category', 'amount', 'timestamp']
        for col in required_columns:
            if col not in transactions_df.columns:
                print(f"Warning: '{col}' column not found in transactions data")
                if col == 'category':
                    transactions_df['category'] = 'Unknown'
                elif col == 'amount':
                    transactions_df['amount'] = 0.0
                elif col == 'timestamp':
                    transactions_df['timestamp'] = datetime.now().isoformat()
        
        # Mark anomalies and ensure it's a boolean type
        transactions_df['is_anomaly'] = transactions_df.apply(
            lambda row: bool(row.get('is_anomaly', False)), axis=1
        )
        
        # Ensure all required columns have proper types
        if 'amount' in transactions_df.columns:
            transactions_df['amount'] = pd.to_numeric(transactions_df['amount'], errors='coerce')
            
        if 'timestamp' in transactions_df.columns:
            transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'], errors='coerce')
        
        # Ensure we have enough data for visualization
        if len(transactions_df) == 0:
            # Create placeholder image for empty data
            plt.figure(figsize=(12, 6))
            plt.text(0.5, 0.5, "No transaction data available", 
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=14)
            plt.axis('off')
            
            # Save figure to bytes
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            plt.close()
            img_bytes.seek(0)
            
            # Convert to base64 for embedding in HTML
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            visualizations['category_amounts'] = f'data:image/png;base64,{img_base64}'
            visualizations['timeline'] = f'data:image/png;base64,{img_base64}'
            
            return visualizations
        
        # Create boxplot using the recommended approach to avoid warnings
        plt.figure(figsize=(12, 6))
        
        # Group by category for cleaner visualization
        categories = transactions_df['category'].unique()
        
        # Create plot per category to avoid seaborn boxplot warnings
        for i, category in enumerate(categories):
            # Filter data for this category
            cat_data = transactions_df[transactions_df['category'] == category]
            
            # Split into normal and anomaly data
            normal_data = cat_data[~cat_data['is_anomaly'].astype(bool)]['amount']
            anomaly_data = cat_data[cat_data['is_anomaly'].astype(bool)]['amount']
            
            # Plot normal data in blue
            if not normal_data.empty:
                position = i - 0.2
                plt.boxplot(normal_data, positions=[position], widths=0.3, 
                           patch_artist=True, boxprops=dict(facecolor='skyblue'))
            
            # Plot anomaly data in red
            if not anomaly_data.empty:
                position = i + 0.2
                plt.boxplot(anomaly_data, positions=[position], widths=0.3,
                           patch_artist=True, boxprops=dict(facecolor='salmon'))
        
        # Add labels and legend
        plt.title('Transaction Amounts by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.xticks(range(len(categories)), categories, rotation=45)
        
        # Create custom legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='skyblue', label='Normal'),
            Patch(facecolor='salmon', label='Anomaly')
        ]
        plt.legend(handles=legend_elements, title='Transaction Type')
        plt.tight_layout()
        
        # Save figure to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)
        
        # Convert to base64 for embedding in HTML
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
        visualizations['category_amounts'] = f'data:image/png;base64,{img_base64}'
        
        # Transaction timeline
        plt.figure(figsize=(12, 6))
        
        # Convert timestamps to datetime
        transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
        transactions_df = transactions_df.sort_values('timestamp')
        
        # Filter normal transactions first to avoid data type issues
        normal_df = transactions_df[~transactions_df['is_anomaly'].astype(bool)]
        
        # Plot transaction amounts over time
        plt.scatter(
            normal_df['timestamp'], 
            normal_df['amount'],
            alpha=0.7, label='Normal'
        )
        
        # Plot anomalies
        if 'is_anomaly' in transactions_df.columns:
            anomalies = transactions_df[transactions_df['is_anomaly']]
            if not anomalies.empty:
                plt.scatter(
                    anomalies['timestamp'], 
                    anomalies['amount'],
                    color='red', marker='*', s=100, label='Anomaly'
                )
        
        plt.title('Transaction Timeline')
        plt.xlabel('Time')
        plt.ylabel('Amount ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save figure to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)
        
        # Convert to base64
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
        visualizations['timeline'] = f'data:image/png;base64,{img_base64}'
    
    except Exception as e:
        import traceback
        print(f"Error creating visualizations: {str(e)}")
        print(traceback.format_exc())
        
        # Create error image
        plt.figure(figsize=(12, 6))
        plt.text(0.5, 0.5, f"Error creating visualization: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=12, color='red')
        plt.axis('off')
        
        # Save figure to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)
        
        # Convert to base64
        img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
        visualizations['category_amounts'] = f'data:image/png;base64,{img_base64}'
        visualizations['timeline'] = f'data:image/png;base64,{img_base64}'
    
    return visualizations

def create_sample_test_history(history_file, test_names=None):
    """Create a sample test history file for demonstration."""
    if test_names is None or not test_names:
        test_names = [
            'test_login', 'test_invalid_login', 'test_transfer', 
            'test_account_details', 'test_api_auth', 'test_health'
        ]
    
    # Create a list of modules
    modules = ['ui', 'api', 'smoke']
    
    # Generate sample history
    import random
    
    history = []
    for i in range(100):
        test_name = random.choice(test_names)
        module = random.choice(modules)
        
        # Make certain tests fail more often
        if test_name == 'test_transfer' and module == 'ui':
            result = random.choices(['pass', 'fail'], weights=[0.6, 0.4])[0]
        elif test_name == 'test_api_auth' and module == 'api':
            result = random.choices(['pass', 'fail'], weights=[0.7, 0.3])[0]
        else:
            result = random.choices(['pass', 'fail'], weights=[0.9, 0.1])[0]
        
        duration = random.uniform(0.1, 5.0)
        timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        
        history.append({
            'test_name': test_name,
            'module': module,
            'result': result,
            'duration': duration,
            'timestamp': timestamp
        })
    
    # Save to file
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    pd.DataFrame(history).to_csv(history_file, index=False)
    
    return history_file

def generate_test_failure_rates(history_file, tests):
    """Generate a visualization of test failure rates."""
    history_df = pd.read_csv(history_file)
    
    # Extract test names from fully qualified test paths
    test_names = []
    for test in tests:
        if '::' in test:
            parts = test.split('::')
            test_name = parts[-1]
            module = parts[0].split('/')[-2] if '/' in parts[0] else 'unknown'
        else:
            test_name = test
            module = 'unknown'
        test_names.append((test, test_name, module))
    
    # Calculate failure rates
    failure_rates = []
    for test, test_name, module in test_names:
        test_history = history_df[(history_df['test_name'] == test_name) & 
                                 (history_df['module'] == module)]
        
        if not test_history.empty:
            failure_rate = (test_history['result'] == 'fail').mean()
        else:
            failure_rate = 0
        
        failure_rates.append((test, failure_rate))
    
    # Sort by failure rate
    failure_rates.sort(key=lambda x: x[1], reverse=True)
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    tests = [t[0].split('::')[-1] for t in failure_rates]
    rates = [t[1] for t in failure_rates]
    
    plt.bar(tests, rates, color='skyblue')
    plt.title('Test Failure Rates')
    plt.xlabel('Test')
    plt.ylabel('Failure Rate')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save figure to bytes
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    
    return f'data:image/png;base64,{img_base64}'

def generate_sample_response_times():
    """Generate sample API response times with anomalies."""
    np.random.seed(42)
    
    # Generate normal response times with occasional spikes
    n_samples = 100
    response_times = np.random.lognormal(mean=-1.5, sigma=0.4, size=n_samples)
    
    # Add some anomalies
    anomaly_indices = np.random.choice(range(n_samples), size=5, replace=False)
    for idx in anomaly_indices:
        response_times[idx] = response_times[idx] * np.random.uniform(3, 10)
    
    return response_times.tolist()

def detect_response_time_anomalies(response_times):
    """Detect anomalies in API response times using Isolation Forest."""
    from sklearn.ensemble import IsolationForest
    
    # Convert to numpy array
    X = np.array(response_times).reshape(-1, 1)
    
    # Fit isolation forest
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    
    # Predict anomalies
    predictions = model.predict(X)
    anomaly_indices = [i for i, pred in enumerate(predictions) if pred == -1]
    anomalies = [response_times[i] for i in anomaly_indices]
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    plt.scatter(range(len(response_times)), response_times, 
               c=['red' if i in anomaly_indices else 'blue' for i in range(len(response_times))], 
               alpha=0.7)
    plt.title('API Response Time Anomalies')
    plt.xlabel('Request #')
    plt.ylabel('Response Time (s)')
    plt.grid(True, alpha=0.3)
    
    # Save figure to bytes
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    visualization = f'data:image/png;base64,{img_base64}'
    
    return anomalies, visualization

def detect_transaction_anomalies(transactions):
    """Detect anomalies in banking transactions."""
    # Extract amounts and timestamps
    amounts = [t['amount'] for t in transactions]
    
    # Use Isolation Forest for anomaly detection
    from sklearn.ensemble import IsolationForest
    
    # Convert to numpy array
    X = np.array(amounts).reshape(-1, 1)
    
    # Fit isolation forest
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    
    # Predict anomalies
    predictions = model.predict(X)
    anomaly_indices = [i for i, pred in enumerate(predictions) if pred == -1]
    anomalies = [transactions[i] for i in anomaly_indices]
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    
    # Create a dataframe
    df = pd.DataFrame(transactions)
    
    # Add anomaly flag
    df['is_anomaly'] = False
    for idx in anomaly_indices:
        df.loc[idx, 'is_anomaly'] = True
    
    # Convert timestamps if present
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    
    # Plot transaction amounts
    plt.scatter(
        range(len(df[~df['is_anomaly']])), 
        df[~df['is_anomaly']]['amount'],
        alpha=0.7, label='Normal'
    )
    
    # Plot anomalies
    anomalies_df = df[df['is_anomaly']]
    if not anomalies_df.empty:
        plt.scatter(
            range(len(df) - len(anomalies_df), len(df)), 
            anomalies_df['amount'],
            color='red', marker='*', s=100, label='Anomaly'
        )
    
    plt.title('Transaction Amount Anomalies')
    plt.xlabel('Transaction #')
    plt.ylabel('Amount ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save figure to bytes
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    
    # Convert to base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    visualization = f'data:image/png;base64,{img_base64}'
    
    return anomalies, visualization

if __name__ == '__main__':
    app.run(debug=True, port=5000)
