# SV13 Admin Suite - SETEC Institute

A Streamlit-based Active Directory and Exchange Server user management system for SETEC Institute.

## Features

- **Bulk Import**: Upload CSV/Excel files to bulk create AD users
- **Manual Entry**: Add users one at a time
- **Smart Detection**: Automatically detects Name and Department columns
- **Bilingual UI**: English + Khmer language support
- **Script Generation**: Ready-to-run PowerShell scripts for AD and Exchange

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run server_suite.py
```

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- openpyxl (for Excel support)

## License

© 2026 SETEC Institute | Developed by Eab Rithea

