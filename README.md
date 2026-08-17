# 📊 DataPulse

### Intelligent Data Quality, Profiling & Validation Platform
# DataPulse

🚀 **Live Demo:** https://datapulse-production-1541.up.railway.app/

DataPulse is a Django-based data quality platform designed to help users **upload datasets, analyze their structure, detect data-quality issues, execute validation rules, and understand overall dataset quality through an interactive dashboard.**

The project focuses on automating common data-quality checks such as **missing values, duplicate records, invalid formats, and range violations**, while providing measurable validation results through quality scores and issue statistics.

---

## 🚀 Overview

Data quality becomes increasingly difficult to manage as datasets grow in size.

DataPulse provides a centralized workflow for analyzing and validating datasets:

```text
Upload Dataset
      ↓
Read Dataset
      ↓
Profile Dataset
      ↓
Run Validation
      ↓
Detect Data Issues
      ↓
Calculate Quality Score
      ↓
Display Results
```

The application combines **Django, Python, Pandas, MySQL, and custom validation algorithms** to provide an end-to-end data-quality workflow.

---

# ✨ Key Features

### 📁 Dataset Upload

* Upload datasets through the web interface
* Store dataset information in the database
* Process uploaded data using the DataPulse processing pipeline

### 🔍 Dataset Profiling

Analyze uploaded datasets to understand:

* Number of records
* Columns
* Data types
* Missing values
* Duplicate information
* Dataset structure

### 🧪 Automated Data Validation

DataPulse detects multiple categories of data-quality problems:

* Missing values
* Duplicate records
* Range violations
* Invalid formats

### 📏 Configurable Validation Rules

Validation rules can be stored and managed through the database.

Examples include:

* Email format validation
* Required-value validation
* Unique-record validation
* Age-range validation

### 📊 Quality Score

After validation, DataPulse generates:

* Total checks
* Passed checks
* Failed checks
* Quality score
* Issue counts by category
* Total detected issues

### 📈 Interactive Dashboard

The dashboard provides a visual representation of dataset quality and validation results so users can understand problems without manually inspecting every record.

---

# 🧠 Validation Engine

The validation engine is one of the core components of DataPulse.

The project contains dedicated algorithms for different types of data-quality problems.

```text
algorithms/
│
├── duplicate_detector.py
├── format_detector.py
├── missing_value_detector.py
└── range_detector.py
```

---

## 🔴 Missing Value Detection

Detects empty or missing values within dataset columns.

Example:

```text
Name    Age
Sai     21
Ravi
Anu     24
```

The missing `Age` value can be detected by the validation engine.

---

## 🔁 Duplicate Detection

Detects duplicate records or duplicate values based on configured columns.

Example:

```text
Email
----------------
sai@gmail.com
ravi@gmail.com
sai@gmail.com
```

The duplicate email can be identified as a data-quality issue.

---

## 📏 Range Validation

Checks whether numerical values fall within an allowed range.

Example:

```text
Age: 250
Allowed range: 0 - 120
```

The value is identified as a range violation.

---

## 📧 Format Validation

Validates values against expected formats.

For example, email validation can check whether values follow an expected email pattern.

---

# ⚙️ Validation Rules

DataPulse supports database-backed validation rules through the `ValidationRule` model.

Example rules implemented in the project include:

### EMAIL_FORMAT

```text
Code: EMAIL_FORMAT
Type: format
Column: email
```

Validates email values using a configured regular-expression pattern.

### REQUIRED_VALUE

```text
Code: REQUIRED_VALUE
Type: missing
```

Detects missing values.

### UNIQUE_RECORD

```text
Code: UNIQUE_RECORD
Type: duplicate
Columns: email
```

Detects duplicate email values.

### AGE_RANGE

```text
Code: AGE_RANGE
Type: range
Column: age
Minimum: 0
Maximum: 120
```

Validates that age values fall within the configured range.

---

# 📊 Example Validation Result

DataPulse has been tested locally with a large dataset containing **500,000 records**.

Example result:

```text
Total Checks : 500,000
Passed       : 499,689
Failed       : 311
Quality      : 99.94%
```

Issue breakdown:

```text
Missing Values       : 194
Duplicate Records    : 54
Range Violations     : 8
Invalid / Format     : 55
Total Issues         : 311
```

This demonstrates the application's ability to process a large dataset and identify multiple categories of data-quality problems.

---

# 🏗️ Project Architecture

```text
                         ┌─────────────────────┐
                         │    Web Interface    │
                         │ HTML / CSS / JS     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Django         │
                         │ Views / APIs        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │  Data Engine    │             │ Validation      │
          │                 │             │ Service         │
          │ Reader          │             │                 │
          │ Profiler        │             │ Validation      │
          │ Processor       │             │ Engine          │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │      MySQL          │
                         │                     │
                         │ Dataset             │
                         │ ValidationRule      │
                         │ ValidationRun       │
                         │ DataIssue           │
                         └─────────────────────┘
```

---

# 📁 Project Structure

```text
DataPulse/
│
├── algorithms/
│   ├── __init__.py
│   ├── duplicate_detector.py
│   ├── format_detector.py
│   ├── missing_value_detector.py
│   └── range_detector.py
│
├── apps/
│   ├── __init__.py
│   │
│   ├── accounts/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   ├── datasets_app/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── reports_app/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   │
│   └── validation/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── data_engine/
│   ├── __init__.py
│   ├── processor.py
│   ├── profiler.py
│   └── reader.py
│
├── datasets/
│   └── sample/
│       ├── duplicates.csv
│       ├── missing_values.csv
│       ├── range_test.csv
│       ├── test.csv
│       └── validation_test.csv
│
├── services/
│   ├── validation_engine.py
│   └── validation_service.py
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── test_duplicates.py
│   ├── test_missing_values.py
│   ├── test_processor.py
│   ├── test_profiler.py
│   ├── test_range.py
│   ├── test_reader.py
│   ├── test_upload_api.py
│   ├── test_validation_engine.py
│   └── test_validation_service.py
│
├── manage.py
├── requirements.txt
└── .gitignore
```

---

# 🧩 Django Applications

## Accounts

Handles account-related functionality.

```text
apps/accounts/
```

## Datasets

Responsible for dataset-related functionality.

```text
apps/datasets_app/
```

## Validation

Contains the main validation models, rules, migrations, URLs, views, and validation functionality.

```text
apps/validation/
```

Important database entities include:

```text
ValidationRule
ValidationRun
DataIssue
```

## Reports

Contains reporting-related application components.

```text
apps/reports_app/
```

---

# ⚙️ Data Engine

The data-processing layer is located under:

```text
data_engine/
```

### `reader.py`

Responsible for reading dataset files.

### `profiler.py`

Responsible for analyzing dataset characteristics.

### `processor.py`

Responsible for processing dataset information as part of the DataPulse pipeline.

---

# 🔧 Service Layer

The service layer is located under:

```text
services/
```

### `validation_engine.py`

Coordinates the validation algorithms.

### `validation_service.py`

Provides the higher-level validation workflow and validation result generation.

---

# 🗄️ Database

DataPulse uses **MySQL** for its database layer.

The database stores application information such as:

* Dataset records
* Validation rules
* Validation runs
* Data-quality issues

Production-sensitive database credentials are handled through environment variables rather than being hardcoded into the source code.

---

# 🔐 Environment Configuration

Sensitive configuration should be stored using environment variables.

Example:

```text
DB_NAME=datapulse_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
```

> Never commit real database passwords or other secrets to GitHub.

---

# 🧪 Testing

DataPulse contains tests covering the major processing and validation components.

Test areas include:

* Duplicate detection
* Missing-value detection
* Range validation
* Dataset reading
* Dataset profiling
* Dataset processing
* Validation engine
* Validation service
* Upload API

Run the test suite with:

```cmd
python manage.py test
```

---

# 💻 Local Setup

## 1. Clone the repository

```cmd
git clone https://github.com/sailakshmi78/DataPulse.git
cd DataPulse
```

## 2. Create a virtual environment

```cmd
python -m venv venv
```

## 3. Activate the virtual environment

```cmd
venv\Scripts\activate
```

## 4. Install dependencies

```cmd
python -m pip install -r requirements.txt
```

## 5. Configure MySQL

Create the required MySQL database and configure the database environment variables.

Example:

```text
DB_NAME=datapulse_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

## 6. Run migrations

```cmd
python manage.py migrate
```

## 7. Start the Django development server

```cmd
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 📦 Sample Datasets

The project contains sample datasets for testing the validation algorithms.

```text
datasets/sample/
```

Available examples include:

```text
duplicates.csv
missing_values.csv
range_test.csv
test.csv
validation_test.csv
```

These datasets can be used to verify individual validation scenarios during development.

---

# 🛠️ Technology Stack

| Category             | Technology                           |
| -------------------- | ------------------------------------ |
| Programming Language | Python                               |
| Backend Framework    | Django                               |
| API                  | Django REST Framework                |
| Data Processing      | Pandas                               |
| Numerical Processing | NumPy                                |
| Database             | MySQL                                |
| Frontend             | HTML, CSS, JavaScript                |
| Server               | Django Development Server / Gunicorn |
| Static Files         | WhiteNoise                           |
| Testing              | Django Test Framework                |
| Version Control      | Git                                  |
| Repository           | GitHub                               |
| IDE                  | VS Code                              |

---

# 🎯 Project Goals

The main goals of DataPulse are:

1. Automate common data-quality checks.
2. Reduce manual dataset inspection.
3. Provide configurable validation rules.
4. Generate measurable dataset-quality scores.
5. Identify and categorize data-quality issues.
6. Provide a simple dashboard for understanding validation results.
7. Build a scalable foundation for future data-quality analytics.

---

# 🔮 Future Enhancements

Potential future improvements include:

* More validation rule types
* Advanced data profiling
* Additional file formats
* Automated report generation
* Exportable validation reports
* Background processing for very large datasets
* User-specific dataset management
* Validation history and trend analysis
* Advanced data-quality analytics
* Improved authentication and authorization
* Cloud deployment

---

# 📌 Current Project Status

```text
Django Application       ✅
MySQL Integration        ✅
Dataset Upload           ✅
Dataset Profiling        ✅
Missing Value Detection  ✅
Duplicate Detection      ✅
Range Detection          ✅
Format Detection         ✅
Validation Rules         ✅
Quality Scoring          ✅
Validation Dashboard     ✅
Automated Tests          ✅
GitHub Repository        ✅

Production Deployment    ⏸️ Not currently deployed
```

---

# 👨‍💻 Developer

## Sai Lakshmi Karanam

**Python Developer | Backend Developer | AI & ML Graduate**

GitHub:
https://github.com/sailakshmi78

LinkedIn:
https://www.linkedin.com/in/sailakshmi-karanam-907a26271/

---

# ⭐ DataPulse

> **Upload. Profile. Validate. Detect. Score. Understand.**

DataPulse transforms raw datasets into meaningful data-quality insights through automated profiling and validation.
