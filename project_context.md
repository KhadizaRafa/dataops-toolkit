# DataOps Toolkit - Project Context

## Project Overview
**Name**: DataOps Toolkit
**Description**: A modular Python automation framework for QA/SDETs to validate, transform, and merge data (CSV, JSON, Excel).
**Goal**: Portfolio project demonstrating clean architecture, testing, CI/CD, and CLI tools.

## Key Features
1.  **Converters**: CSV <-> JSON <-> Excel.
2.  **Merger**: Merge multiple files, with SQL-style join support (`--on`, `--how`).
3.  **Validator**: Check for duplicates and missing values.
4.  **CLI**: `dataops` command line interface.
5.  **Logging**: Logs saved to `logs/` directory.

## Directory Structure
```
dataops-toolkit/
├── src/dataops/
│   ├── converters/
│   │   ├── csv_to_json.py
│   │   └── json_to_excel.py  # Function: convert_json_to_excel(input, output, fields=None)
│   ├── merger/
│   │   └── merge_files.py    # Function: merge_csv_files(inputs, output, join_on=None, how='inner')
│   ├── validator/
│   │   └── validate_data.py
│   ├── utils/
│   │   ├── logger.py         # Sets up file and stream handlers
│   │   └── file_io.py        # Safe read/write wrappers
│   └── cli.py                # Click-based CLI entry point
│
├── tests/                    # Pytest suite covering all modules
├── logs/                     # Auto-generated logs
├── requirements.txt
├── setup.py                  # Package config
└── README.md
```

## Core Dependencies
- `pandas`: Data manipulation
- `openpyxl`: Excel I/O
- `click`: CLI framework
- `pytest`: Testing

## Quick Start
```bash
pip install -e .
dataops --help
```

## Example Usage
- **Merge**: `dataops merge a.csv b.csv out.csv --on id --how left`
- **JSON->Excel**: `dataops json-to-excel in.json out.xlsx --fields "key=id"`
