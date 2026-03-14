# SV13 Admin Suite v2.0 - Professional Edition | SETEC Institute

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sv13-app-suite-tyka8pz4tearxepnjaauzb.streamlit.app/)

Professional Active Directory & Exchange Server user provisioning system with UPN conflict resolution, safety CSV export, and bilingual (English/Khmer) UI.

## Features

- **Bulk Import**: Upload CSV/Excel files to bulk create AD users
- **Manual Entry**: Add users one at a time
- **Smart Detection**: Automatically detects Name and Department columns
- **Bilingual UI**: English + Khmer language support
- **Script Generation**: Ready-to-run PowerShell scripts for AD and Exchange

## 🚀 Quick Start (Local)

```bash
cd Net/Import-file
pip install -r requirements.txt
streamlit run server_suite.py
```

## ☁️ Production Deployment (Streamlit Cloud)

1. **GitHub Repo Setup**:
   ```
   cd Net/Import-file
   git init
   git add .
   git commit -m "SV13 Admin Suite v2.0 - Professional Edition"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/sv13-admin-suite.git
   git push -u origin main
   ```

2. **Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - "New app" → Deploy from existing repo
   - Select `sv13-admin-suite` repo → main branch → `server_suite.py`
   - Click **Deploy**

3. **Verify**: https://your-app-name.streamlit.app

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- openpyxl (for Excel support)

## License

© 2026 SETEC Institute | Developed by Eab Rithea

