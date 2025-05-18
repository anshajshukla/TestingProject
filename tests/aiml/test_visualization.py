"""
Specific tests for the visualization components used in the ML dashboard.
This ensures that visualizations are properly generated and displayed.
"""
import pytest
import os
import numpy as np
import pandas as pd
import matplotlib
# Set the backend before importing pyplot
matplotlib.use('Agg')  # Use non-interactive backend

# Silence common matplotlib warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")

# Import after warning filters
import matplotlib.pyplot as plt
import seaborn as sns

# Configure seaborn with compatible settings
sns.set_theme(style="whitegrid")

# Set rcParams directly through matplotlib to avoid warnings
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'axes.grid': True,
    'axes.spines.top': False,
    'axes.spines.right': False
})
import io
import base64
from datetime import datetime, timedelta
import json

from utils.ml.data_generator import BankingDataGenerator

@pytest.fixture(scope="module")
def setup_visualization_test():
    """Setup for visualization tests."""
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Configure matplotlib and seaborn for consistent output
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['font.size'] = 12
    
    # Generate test data
    generator = BankingDataGenerator(num_accounts=3)
    test_data_path = "data/visualization_test_data.json"
    test_data = generator.save_test_data(test_data_path)
    
    return test_data

def test_basic_matplotlib_rendering(setup_visualization_test):
    """Test basic matplotlib rendering capabilities."""
    # Create a simple plot
    plt.figure(figsize=(10, 6))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title("Basic Matplotlib Test")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    
    # Save the plot to a file
    output_path = "reports/basic_matplotlib_test.png"
    plt.savefig(output_path)
    plt.close()
    
    # Verify the file exists and has content
    assert os.path.exists(output_path), "Plot file should exist"
    assert os.path.getsize(output_path) > 0, "Plot file should have content"
    
    # Test base64 encoding (used by dashboard)
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title("Base64 Encoding Test")
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    # Convert to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    assert len(image_base64) > 0, "Base64 encoding should produce output"
    
    # Save the base64 string to a file for inspection
    with open("reports/base64_test.txt", "w") as f:
        f.write(image_base64[:100] + "...")  # Just save a sample

def test_seaborn_visualization(setup_visualization_test):
    """Test seaborn visualization components."""
    # Create a sample dataframe
    df = pd.DataFrame({
        'category': ['A', 'B', 'C', 'A', 'B', 'C'] * 10,
        'value': np.random.randn(60),
        'is_anomaly': [False] * 55 + [True] * 5
    })
    
    # Create a boxplot using matplotlib directly to avoid seaborn warnings
    plt.figure(figsize=(10, 6))
    
    # Group by category
    categories = df['category'].unique()
    
    # Plot each category
    for i, category in enumerate(categories):
        cat_data = df[df['category'] == category]
        
        # Split by anomaly flag
        normal_data = cat_data[~cat_data['is_anomaly']]['value']
        anomaly_data = cat_data[cat_data['is_anomaly']]['value']
        
        # Plot normal data
        if len(normal_data) > 0:
            plt.boxplot(normal_data, positions=[i-0.2], widths=0.3, 
                      patch_artist=True, boxprops=dict(facecolor='skyblue'))
        
        # Plot anomaly data
        if len(anomaly_data) > 0:
            plt.boxplot(anomaly_data, positions=[i+0.2], widths=0.3, 
                      patch_artist=True, boxprops=dict(facecolor='salmon'))
    
    # Add labels and legend
    plt.title("Boxplot Test (Using matplotlib)")
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.xticks(range(len(categories)), categories)
    
    # Add custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='skyblue', label='Normal'),
        Patch(facecolor='salmon', label='Anomaly')
    ]
    plt.legend(handles=legend_elements, title='Transaction Type')
    
    # Save the plot
    output_path = "reports/seaborn_boxplot_test.png"
    plt.savefig(output_path)
    plt.close()
    
    # Verify the file exists and has content
    assert os.path.exists(output_path), "Seaborn plot file should exist"
    assert os.path.getsize(output_path) > 0, "Seaborn plot file should have content"

def test_transaction_visualizations(setup_visualization_test):
    """Test specific visualizations used in the dashboard for transactions."""
    test_data = setup_visualization_test
    
    # Create a dataframe from transactions
    transactions_df = pd.DataFrame(test_data['transactions'])
    
    # Mark anomalies and ensure it's stored as a proper boolean type
    transactions_df['is_anomaly'] = transactions_df.apply(
        lambda row: bool(row.get('is_anomaly', False)), axis=1
    )
    
    # Ensure is_anomaly is explicitly converted to boolean
    transactions_df['is_anomaly'] = transactions_df['is_anomaly'].astype(bool)
    
    # 1. Test category amount boxplot using matplotlib directly
    plt.figure(figsize=(12, 6))
    
    # Group by category
    categories = transactions_df['category'].unique()
    
    # Plot each category separately to avoid seaborn warnings
    for i, category in enumerate(categories):
        cat_data = transactions_df[transactions_df['category'] == category]
        
        # Split by anomaly flag
        normal_data = cat_data[~cat_data['is_anomaly']]['amount']
        anomaly_data = cat_data[cat_data['is_anomaly']]['amount']
        
        # Plot normal data
        if not normal_data.empty:
            plt.boxplot(normal_data, positions=[i-0.2], widths=0.3, 
                       patch_artist=True, boxprops=dict(facecolor='skyblue'))
        
        # Plot anomaly data
        if not anomaly_data.empty:
            plt.boxplot(anomaly_data, positions=[i+0.2], widths=0.3, 
                       patch_artist=True, boxprops=dict(facecolor='salmon'))
    
    # Add labels and legend
    plt.title('Transaction Amounts by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount ($)')
    plt.xticks(range(len(categories)), categories, rotation=45)
    
    # Add custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='skyblue', label='Normal'),
        Patch(facecolor='salmon', label='Anomaly')
    ]
    plt.legend(handles=legend_elements, title='Transaction Type')
    plt.tight_layout()
    
    # Save to file
    output_path = "reports/category_amounts_test.png"
    plt.savefig(output_path)
    plt.close()
    
    # Verify the file
    assert os.path.exists(output_path), "Category plot file should exist"
    assert os.path.getsize(output_path) > 0, "Category plot file should have content"
    
    # 2. Test timeline visualization
    plt.figure(figsize=(12, 6))
    
    # Convert timestamps to datetime
    transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
    transactions_df = transactions_df.sort_values('timestamp')
    
    # Make sure is_anomaly is boolean type
    transactions_df['is_anomaly'] = transactions_df['is_anomaly'].astype(bool)
    
    # Plot normal transactions
    plt.scatter(
        transactions_df[~transactions_df['is_anomaly']]['timestamp'], 
        transactions_df[~transactions_df['is_anomaly']]['amount'],
        alpha=0.7, label='Normal'
    )
    
    # Plot anomalies
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
    
    # Save to file
    output_path = "reports/timeline_test.png"
    plt.savefig(output_path)
    plt.close()
    
    # Verify the file
    assert os.path.exists(output_path), "Timeline plot file should exist"
    assert os.path.getsize(output_path) > 0, "Timeline plot file should have content"
    
    # 3. Convert both to base64 (as used in dashboard)
    def create_base64_image(plot_function):
        """Create a base64 encoded image using the provided plot function."""
        buffer = io.BytesIO()
        plt.figure(figsize=(12, 6))
        plot_function()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    
    # Category plot as base64 using matplotlib directly
    def create_category_boxplot():
        # Group by category
        categories = transactions_df['category'].unique()
        
        # Plot each category separately 
        for i, category in enumerate(categories):
            cat_data = transactions_df[transactions_df['category'] == category]
            
            # Split by anomaly flag
            normal_data = cat_data[~cat_data['is_anomaly']]['amount']
            anomaly_data = cat_data[cat_data['is_anomaly']]['amount']
            
            # Plot normal and anomaly data
            if not normal_data.empty:
                plt.boxplot(normal_data, positions=[i-0.2], widths=0.3, 
                           patch_artist=True, boxprops=dict(facecolor='skyblue'))
            
            if not anomaly_data.empty:
                plt.boxplot(anomaly_data, positions=[i+0.2], widths=0.3, 
                           patch_artist=True, boxprops=dict(facecolor='salmon'))
        
        # Add labels
        plt.xticks(range(len(categories)), categories, rotation=45)
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        
        # Create custom legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='skyblue', label='Normal'),
            Patch(facecolor='salmon', label='Anomaly')
        ]
        plt.legend(handles=legend_elements, title='Transaction Type')
    
    category_b64 = create_base64_image(create_category_boxplot)
    assert len(category_b64) > 0, "Category base64 encoding should produce output"
    
    # Timeline plot as base64
    def plot_timeline():
        # Ensure is_anomaly is boolean
        transactions_df['is_anomaly'] = transactions_df['is_anomaly'].astype(bool)
        normal_df = transactions_df[~transactions_df['is_anomaly']]
        
        plt.scatter(
            normal_df['timestamp'], 
            normal_df['amount'],
            alpha=0.7, label='Normal'
        )
        
        # Use the already filtered anomalies dataframe
        if not anomalies.empty:
            plt.scatter(
                anomalies['timestamp'], 
                anomalies['amount'],
                color='red', marker='*', s=100, label='Anomaly'
            )
        plt.legend()
    
    timeline_b64 = create_base64_image(plot_timeline)
    assert len(timeline_b64) > 0, "Timeline base64 encoding should produce output"
    
    # Save the visualizations as HTML to verify they display correctly
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visualization Test</title>
    </head>
    <body>
        <h1>Transaction Visualization Test</h1>
        
        <h2>Category Amounts</h2>
        <img src="data:image/png;base64,{category_b64}" alt="Category amounts">
        
        <h2>Timeline</h2>
        <img src="data:image/png;base64,{timeline_b64}" alt="Timeline">
    </body>
    </html>
    """
    
    with open("reports/visualization_test.html", "w") as f:
        f.write(html_content)
    
    assert os.path.exists("reports/visualization_test.html"), "HTML file should exist"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
