# DataOps Toolkit — A Modular Automation Framework

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

> A Python-based automation toolkit designed for validating, transforming, merging, and converting structured data. Built with extensibility and reusability in mind.

## 🚀 Features

- **Data Conversion**: Seamlessly convert between CSV, JSON, and Excel formats.
- **Data Merging**: Merge multiple CSV or Excel files into unified datasets.
- **Data Validation**: Automatically detect duplicates and missing values.
- **Modular Architecture**: Designed for easy extension and integration into larger pipelines.
- **CLI Interface**: Powerful command-line tools for quick operations.

## 📦 Installation

To install the toolkit, clone the repository and install it using pip:

```bash
git clone https://github.com/yourusername/dataops-toolkit.git
cd dataops-toolkit
pip install .
```

For development (including testing tools):

```bash
pip install -e .[dev]
```

## 🛠 Usage

The toolkit exposes a `dataops` command.

### Convert CSV to JSON
```bash
dataops csv-to-json input.csv output.json
```

### Convert JSON to Excel
```bash
# Basic conversion
dataops json-to-excel input.json output.xlsx

# With field mapping (rename 'key' to 'id', 'doc_count' to 'count')
dataops json-to-excel input.json output.xlsx --json-fields "key,doc_count" --output-headers "id,count"
```

### Merge Files
```bash
# Simple concatenation
dataops merge file1.csv file2.csv output.csv

# Advanced Join (e.g., Left Join on 'id')
dataops merge file1.csv file2.csv output.csv --on id --how left
```

### Validate Data
```bash
dataops validate input.csv
```

## 🏗 Project Structure

```
dataops-toolkit/
│
├── src/dataops/          # Source code
│   ├── converters/       # Conversion logic
│   ├── merger/           # Merging logic
│   ├── validator/        # Validation logic
│   └── utils/            # Shared utilities (logging, file I/O)
│
├── tests/                # Unit tests (pytest)
├── requirements.txt      # Dependencies
├── setup.py              # Package configuration
└── .github/workflows/    # CI/CD configuration
```

## 🧪 Testing

Run the test suite using pytest:

```bash
pytest
```

## 🔑 Key Concepts

- **Python Automation**: Automate repetitive data tasks.
- **ETL Pipeline**: Extract, Transform, Load capabilities.
- **QA Automation**: Built for testing and validation workflows.
- **Clean Code**: Modular, consistently styled, and documented.

---
Built with ❤️ by a QA Automation Engineer.
