# System Resource Monitoring with Database Logging & API Alerting

## 📌 Overview
This project is an automated system monitoring solution built with Python. It continuously tracks system hardware metrics (CPU and RAM usage), automatically logs high-resource events into a **SQLite database**, and sends real-time HTTP POST alerts via **API Webhooks** (e.g., Discord or Webhook services).

## 🚀 Key Features
- **Resource Monitoring:** Real-time metrics collection using `psutil`.
- **Database Logging:** Automatic event tracking into a local SQLite database (`system_events.db`).
- **API Integration:** Sends structured JSON payloads via HTTP POST requests to trigger real-time alerts.
- **Configurable Thresholds:** Easily adjust CPU/RAM limit triggers via environment variables.
- **Robust Error Handling:** Implements `try-except` blocks to prevent script failures during network or DB connection issues.

## 📁 Project Structure
```text
automation-api/
├── monitor_and_alert.py   # Main Python monitoring script
├── system_events.db       # SQLite database file (excluded in .gitignore)
└── README.md              # Project documentation

## 🛠️ Prerequisites
Ensure Python 3.x and the required packages are installed:
pip install psutil requests

##🧰 How to Run
1.(Optional) Set Custom Webhook URL:
Pass your Webhook URL as an environment variable (defaults to test endpoint if unset):
export ALERT_WEBHOOK_URL="https://webhook.site/4a3bcaf7-1afd-42ab-92a4-3d15ff58e750"

2.Execute Monitoring Script:
python monitor_and_alert.py

3.Query Alert Records from Database:
python -c "import sqlite3; conn = sqlite3.connect('system_events.db'); print(conn.cursor().execute('SELECT * FROM system_alerts').fetchall())"

##🛠️ Troubleshooting & Key Learnings
Dynamic API Configuration: Avoided hardcoding secret Webhook URLs by using os.getenv("ALERT_WEBHOOK_URL") to maintain security best practices.

HTTP Payload Structuring: Formatted JSON payloads compatible with standard Webhook providers to ensure successful delivery without 400 Bad Request errors.