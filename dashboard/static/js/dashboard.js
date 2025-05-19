/**
 * Dashboard application for Banking Test Framework ML components
 * Handles UI interactions for data generation, anomaly detection, and test prioritization
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all sections
    initializeDataGeneration();
    initializeAnomalyDetection();
    initializeTestPrioritization();
    loadDataFiles();
    
    // Handle navigation
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

/**
 * Initialize data generation form and handlers
 */
function initializeDataGeneration() {
    const form = document.getElementById('data-generation-form');
    const results = document.getElementById('data-generation-results');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
        submitButton.disabled = true;
        
        // Get form values
        const numAccounts = document.getElementById('num-accounts').value;
        const transactionsPerDay = document.getElementById('transactions-per-day').value;
        const numDays = document.getElementById('num-days').value;
        
        // Prepare form data
        const formData = new FormData();
        formData.append('num_accounts', numAccounts);
        formData.append('transactions_per_day', transactionsPerDay);
        formData.append('num_days', numDays);
        
        // Make API request
        fetch('/api/generate-data', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            
            if (data.status === 'success') {
                // Show results
                results.style.display = 'block';
                
                // Update message
                document.getElementById('data-generation-message').textContent = data.message;
                
                // Update stats
                document.getElementById('stat-accounts').textContent = data.stats.num_accounts;
                document.getElementById('stat-transactions').textContent = data.stats.num_transactions;
                document.getElementById('stat-anomalies').textContent = data.stats.num_anomalies;
                document.getElementById('stat-value').textContent = '$' + data.stats.total_value.toFixed(2);
                document.getElementById('stat-avg-transaction').textContent = '$' + data.stats.avg_transaction.toFixed(2);
                
                // Update filename
                document.getElementById('data-filename').value = data.filename;
                
                // Update visualizations
                document.getElementById('viz-category-amounts').src = data.visualizations.category_amounts;
                document.getElementById('viz-timeline').src = data.visualizations.timeline;
                
                // Refresh data files list
                loadDataFiles();
                
                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            console.error('Error:', error);
            alert('An error occurred during data generation.');
        });
    });
}

/**
 * Initialize anomaly detection form and handlers
 */
function initializeAnomalyDetection() {
    const form = document.getElementById('anomaly-detection-form');
    const results = document.getElementById('anomaly-detection-results');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Detecting...';
        submitButton.disabled = true;
        
        // Get form values
        const dataType = document.getElementById('data-type').value;
        const dataFile = document.getElementById('data-file').value;
        
        // Prepare form data
        const formData = new FormData();
        formData.append('data_type', dataType);
        formData.append('data_file', dataFile);
        
        // Make API request
        fetch('/api/anomaly-detection', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            
            if (data.status === 'success') {
                // Show results
                results.style.display = 'block';
                
                // Update message
                document.getElementById('anomaly-message').textContent = data.message;
                
                // Update visualization
                document.getElementById('anomaly-visualization').src = data.visualization;
                
                // Update anomaly table
                const tableBody = document.querySelector('#anomaly-table tbody');
                tableBody.innerHTML = '';
                
                if (dataType === 'response_times') {
                    // For response times, show simple values
                    data.anomalies.forEach((anomaly, index) => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${index + 1}</td>
                            <td>${anomaly.toFixed(4)} seconds</td>
                            <td>Unusually ${anomaly > 0.5 ? 'high' : 'low'} response time</td>
                        `;
                        tableBody.appendChild(row);
                    });
                } else {
                    // For transactions, show more details
                    data.anomalies.forEach((anomaly, index) => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${index + 1}</td>
                            <td>$${anomaly.amount.toFixed(2)}</td>
                            <td>${anomaly.description || 'Unusual transaction pattern'}</td>
                        `;
                        tableBody.appendChild(row);
                    });
                }
                
                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            console.error('Error:', error);
            alert('An error occurred during anomaly detection.');
        });
    });
}

/**
 * Initialize test prioritization form and handlers
 */
function initializeTestPrioritization() {
    const form = document.getElementById('test-prioritization-form');
    const results = document.getElementById('test-prioritization-results');
    
    // Set default test list if empty
    const testList = document.getElementById('test-list');
    if (!testList.value) {
        testList.value = `tests/ui/test_login.py::test_valid_login
tests/ui/test_login.py::test_invalid_login
tests/api/test_auth.py::test_login_success
tests/api/test_transactions.py::test_get_transactions
tests/smoke/test_health.py::test_ui_health`;
    }
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Prioritizing...';
        submitButton.disabled = true;
        
        // Get form values
        const tests = document.getElementById('test-list').value;
        
        // Prepare form data
        const formData = new FormData();
        formData.append('tests', tests);
        
        // Make API request
        fetch('/api/prioritize-tests', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            
            if (data.status === 'success') {
                // Show results
                results.style.display = 'block';
                
                // Update message
                document.getElementById('prioritization-message').textContent = data.message;
                
                // Update prioritized tests list
                const testsList = document.getElementById('prioritized-tests');
                testsList.innerHTML = '';
                
                data.prioritized_tests.forEach(test => {
                    const item = document.createElement('li');
                    item.className = 'list-group-item';
                    item.textContent = test;
                    testsList.appendChild(item);
                });
                
                // Update visualization
                document.getElementById('failure-rate-viz').src = data.visualization;
                
                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            console.error('Error:', error);
            alert('An error occurred during test prioritization.');
        });
    });
}

/**
 * Load available data files for selection
 */
function loadDataFiles() {
    fetch('/api/list-data-files')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const dataFileSelect = document.getElementById('data-file');
                
                // Keep the first option
                const firstOption = dataFileSelect.options[0];
                dataFileSelect.innerHTML = '';
                dataFileSelect.appendChild(firstOption);
                
                // Add data files
                data.data_files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file.filename;
                    option.textContent = `${file.filename} (${formatFileSize(file.size)})`;
                    dataFileSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error loading data files:', error);
        });
}

/**
 * Format file size in human-readable format
 */
function formatFileSize(bytes) {
    if (bytes < 1024) {
        return bytes + ' bytes';
    } else if (bytes < 1024 * 1024) {
        return (bytes / 1024).toFixed(1) + ' KB';
    } else {
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
}
