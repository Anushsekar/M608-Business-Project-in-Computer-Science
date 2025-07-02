# 🌐 Global Cyber Threat Dashboard

An interactive Streamlit dashboard for visualizing global cyber threats, financial losses, and live threat intelligence feeds.

## Features
- Visualize cyber attack trends by year, country, and attack type
- Interactive map of global incidents
- Real-time threat intelligence feed (AlienVault OTX)
- Financial loss analysis from netcrime
- IP address lookup against blocklists
- Modular, extensible codebase

## Data Sources
- [Global Cybersecurity Threats 2015–2024 (Kaggle)](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
- [Global Losses From Netcrime (Kaggle)](https://www.kaggle.com/datasets/huzpsb/cybersecurity-incidents-dataset)
- [FireHOL Level 1 IP Blocklist](https://github.com/firehol/blocklist-ipsets)
- [AlienVault OTX (Open Threat Exchange) API](https://otx.alienvault.com/)

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/AnushSekar/cyber-threat-dashboard.git
cd cyber-threat-dashboard
```

### 2. Install dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser at [http://localhost:8501](http://localhost:8501).

## Project Structure
```
├── app.py                # Main Streamlit app
├── components/           # UI components (sidebar, trends, map, etc.)
├── utils/                # Data loading, filtering, blocklist utilities
├── data/                 # Datasets (CSV, blocklist)
├── config.py             # Color and config settings
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## License
This project is for educational use at Gisma University.

---
Developed by Anush Sekar.
