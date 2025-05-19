# 🏦 Banking Test Automation Framework with AI/ML

A production-grade testing framework for banking/fintech applications, featuring:
- **UI, API, and Security Testing**
- **AI/ML-Powered Test Generation & Prioritization**
- **Interactive ML Dashboard** for test analysis
- **CI/CD Ready** with GitHub Actions

---

A comprehensive testing framework designed to automate validation of banking and fintech web applications across UI, API, and security layers. This framework now includes AI/ML-powered testing capabilities with an interactive dashboard.

---

## 🚀 Quick Start

1. **Set up the environment:**
   ```bash
   git clone https://github.com/anshajshukla/TestingProject.git
   cd TestingProject
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   .\venv\Scripts\activate  # Windows
   
   pip install -r requirements.txt
   ```

2. **Run the ML Dashboard:**
   ```bash
   python dashboard/app.py
   # Access at http://localhost:5000
   ```

3. **Run tests:**
   ```bash
   # All tests
   pytest
   
   # Specific test type
   pytest tests/ui/
   pytest tests/api/
   pytest tests/aiml/
   ```

---

## 🛠 CI/CD Pipeline

This project includes a GitHub Actions workflow (`.github/workflows/test.yml`) that runs on every push to `main`:

1. **Automated Testing**
   - Runs smoke, API, and UI tests
   - Generates JUnit XML reports
   - Stores test artifacts for 7 days

2. **Required Secrets** (Set in GitHub > Settings > Secrets):
   - `BASE_URL`: Base URL of the banking app
   - `API_URL`: API endpoint URL
   - `TEST_USERNAME`: Test account username
   - `TEST_PASSWORD`: Test account password

3. **Scheduled Runs**
   - Daily test execution (midnight UTC)
   - On every push/pull request to `main`

---

## 📊 What's Inside?

### Core Components
- **UI Tests**: Selenium WebDriver with Page Object Model
- **API Tests**: RESTful service validation
- **Security Tests**: OWASP Top 10 vulnerability checks
- **AI/ML Modules**: Test data generation, anomaly detection
- **Dashboard**: Real-time test analytics

### Project Structure
```
banking_tests/
├── dashboard/       # ML Testing Dashboard (Flask app)
├── tests/           # Test suites (UI, API, Security, AI/ML)
├── utils/           # Helpers and ML utilities
├── pages/           # Page Object Models
├── data/            # Test datasets
└── reports/         # Test outputs and visualizations
```

---

## 🧠 AI/ML Features

### 1. Smart Test Data Generation
```python
from utils.ml.data_generator import BankingDataGenerator

generator = BankingDataGenerator(num_accounts=100)
test_data = generator.generate_transactions(days=30)
```

### 2. Anomaly Detection
```python
# In tests/aiml/test_anomaly_detection.py
detector = AnomalyDetector()
anomalies = detector.find_anomalies(transaction_data)
```

### 3. Test Prioritization
```python
# In tests/aiml/test_prioritization.py
prioritizer = MLTestPrioritizer()
priority_order = prioritizer.rank_tests(test_history)
```

---

## 📈 ML Dashboard

Access the dashboard after running `python dashboard/app.py`:

1. **Data Generation**: Create realistic banking transactions
2. **Anomaly Detection**: Visualize transaction patterns
3. **Test Analysis**: View test history and failure predictions

![Dashboard Preview](reports/dashboard_preview.png)

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test type
pytest tests/ui/           # UI tests
pytest tests/api/          # API tests
pytest tests/security/     # Security tests
pytest tests/aiml/         # AI/ML tests

# Generate HTML report
pytest --html=reports/report.html
```

---

## 🔒 Security Note
- Never commit sensitive data to version control
- Use environment variables for credentials
- The `.gitignore` is configured to exclude sensitive files

## 📜 License
MIT

---

## 📬 Get Help
For issues or feature requests, please [open an issue](https://github.com/anshajshukla/TestingProject/issues).

---

💡 **Tip**: Check the GitHub Actions tab to monitor test runs and view reports!

- **Step 1:** Read the [Learning Path](docs/learning_path.md) for a phase-by-phase guide to mastering test automation and AI/ML in this project.
- **Step 2:** See [How to Use the Learning Path](docs/how_to_use_learning_path.md) for study tips and best practices.
- **Step 3:** Explore the [ML Dashboard Guide](docs/ml_dashboard_guide.md) for hands-on ML testing and visualization.

---

## 🧭 Project Flow & Module Overview

This project is organized into clear modules, each with a specific role in the testing workflow:

1. **UI Automation (`pages/`, `tests/ui/`)**
   - Implements the Page Object Model for maintainable Selenium UI tests.
   - Example: `login_page.py`, `test_login.py`.
2. **API Testing (`tests/api/`)**
   - Validates RESTful endpoints and business logic.
   - Example: `test_auth.py`.
3. **Security & Smoke Tests (`tests/security/`, `tests/smoke/`)**
   - Checks for vulnerabilities and basic health.
4. **AI/ML-powered Testing (`tests/aiml/`, `utils/ml/`)**
   - `data_generator.py`: Generates realistic test data with ML patterns.
   - `test_prioritizer.py`: Predicts which tests are likely to fail.
   - `test_anomaly_detection.py`: Detects anomalies in API/transaction data.
   - `test_ml_integration.py`: Shows how to use ML utilities in tests.
5. **ML Dashboard (`dashboard/`)**
   - `app.py`: Flask app for interactive ML-powered data generation, anomaly detection, and test prioritization.
   - `templates/`, `static/`: Dashboard UI assets.
6. **Data & Reports (`data/`, `reports/`)**
   - Stores test data, ML models, and generated reports.
7. **Documentation (`docs/`)**
   - Learning path, ML dashboard guide, and phase-by-phase explanations.
8. **Utilities (`utils/`)**
   - Helpers for driver management, config, and data loading.

### Project Flow Diagram

1. **Start** → 2. **Generate Data (ML Dashboard or CLI)** → 3. **Run UI/API/Security Tests** → 4. **Collect Results** → 5. **Analyze with ML (Anomaly Detection, Prioritization)** → 6. **Visualize & Report (Dashboard/Allure)**

---

## Project Structure

```
banking_tests/
├── pages/              # Page Object Models for UI tests
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── transfer_page.py
├── tests/
│   ├── ui/             # Selenium tests
│   │   ├── test_login.py
│   │   ├── test_transfer.py
│   │   └── test_negative_flows.py
│   ├── api/            # API tests
│   │   ├── test_auth.py
│   │   └── test_transactions.py
│   ├── security/       # Security tests
│   │   └── test_sql_injection.py
│   ├── smoke/          # Quick health checks
│   │   └── test_health.py
│   └── aiml/           # AI/ML-powered tests
│       ├── test_anomaly_detection.py
│       └── test_ml_integration.py
├── utils/              # Helpers (driver setup, config, data)
│   ├── driver_factory.py
│   ├── config.py
│   ├── data_loader.py
│   └── ml/             # ML utilities
│       ├── data_generator.py
│       └── test_prioritizer.py
├── dashboard/          # ML Testing Dashboard
│   ├── app.py
│   ├── templates/
│   └── static/
├── data/               # Test data and ML models
├── reports/            # Test reports
├── docs/               # Documentation
│   ├── learning_path.md
│   ├── ml_dashboard_guide.md
│   └── learning_phases/
├── conftest.py         # pytest fixtures & CLI options
├── requirements.txt    # Dependencies
└── README.md
```

## Setup Instructions

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your configuration:
   ```
   BASE_URL=https://demo-bank.com
   API_URL=https://api.demo-bank.com
   USERNAME=testuser
   PASSWORD=Test@123
   ```
5. Create necessary directories for ML components:
   ```
   mkdir -p data reports
   ```

## Running Tests

- Run all tests:
  ```
  pytest
  ```
- Run specific test types:
  ```
  pytest tests/smoke    # Smoke tests
  pytest tests/api      # API tests
  pytest tests/ui       # UI tests
  pytest tests/aiml     # AI/ML tests
  ```
- Generate Allure reports:
  ```
  pytest --alluredir=reports/
  allure serve reports/
  ```

## ML Testing Dashboard

The framework includes an interactive ML testing dashboard that provides access to AI/ML testing capabilities:

- Data generation with realistic banking patterns
- Anomaly detection in API responses and transactions
- ML-powered test prioritization

### Starting the Dashboard

```
python -m dashboard.app
```

Then open your browser to http://localhost:5000

### Dashboard Features

1. **Data Generation**: Create realistic banking test data with ML-based patterns
2. **Anomaly Detection**: Identify unusual patterns in API responses or transactions
3. **Test Prioritization**: Run tests in order of likely failure based on ML predictions

For detailed information on using the ML dashboard, see the [ML Dashboard Guide](docs/ml_dashboard_guide.md).

## Project Development Phases

1. Foundations & Environment Setup
2. Unit & Smoke Tests
3. UI Automation with Selenium
4. API & Data-Driven Testing
5. AI/ML in Testing
6. CI/CD Basics

See the [Learning Path](docs/learning_path.md) for a detailed guide to each phase.

## Contributing

Please follow the Page Object Model pattern for UI tests and keep API tests organized by endpoints.
