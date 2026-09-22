import datetime
import os
import sqlite3
import psutil
import requests

# ==========================================
# CONFIGURATION Settings
# ==========================================
DB_NAME = "system_events.db"
# เปลี่ยนเป็น Discord Webhook URL จริงของคุณได้เลยครับ
WEBHOOK_URL = os.getenv(
    "ALERT_WEBHOOK_URL", "https://webhook.site/4a3bcaf7-1afd-42ab-92a4-3d15ff58e750"
)  # ใช้ URL ทดสอบเป็นค่าเริ่มต้น

CPU_THRESHOLD = 70.0  # เปอร์เซ็นต์เตือนเมื่อ CPU สูงเกิน
RAM_THRESHOLD = 80.0  # เปอร์เซ็นต์เตือนเมื่อ RAM สูงเกิน


# ==========================================
# DATABASE FUNCTIONS
# ==========================================
def init_db():
    """สร้าง Table บันทึก Event หากยังไม่มี"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_usage REAL NOT NULL,
                ram_usage REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()


def save_alert_to_db(timestamp, cpu, ram, status):
    """บันทึกข้อมูล Alert ลง Database"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO system_alerts (timestamp, cpu_usage, ram_usage, status)
                VALUES (?, ?, ?, ?)
            """,
                (timestamp, cpu, ram, status),
            )
            conn.commit()
            print("[+] Successfully saved alert record to Database.")
    except sqlite3.Error as e:
        print(f"[-] Database Error: {e}")


# ==========================================
# API ALERTING FUNCTION
# ==========================================
def send_api_alert(timestamp, cpu, ram):
    """ส่งแจ้งเตือน Alert ผ่าน API (HTTP POST Request)"""
    payload = {
        "username": "DevOps Monitoring Bot",
        "embeds": [
            {
                "title": "🚨 HIGH RESOURCE USAGE DETECTED",
                "color": 15158332,  # สีแดง
                "fields": [
                    {
                        "name": "Timestamp",
                        "value": timestamp,
                        "inline": False,
                    },
                    {"name": "CPU Usage", "value": f"{cpu}%", "inline": True},
                    {"name": "RAM Usage", "value": f"{ram}%", "inline": True},
                ],
            }
        ],
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code in [200, 204]:
            print("[+] API Alert sent successfully!")
        else:
            print(f"[-] Failed to send API Alert. Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[-] API Connection Error: {e}")


# ==========================================
# MAIN EXECUTION
# ==========================================
def check_system_and_alert():
    init_db()

    # ดึงค่า Resource ปัจจุบัน
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] Checking System... CPU: {cpu}% | RAM: {ram}%")

    # ตรวจสอบว่าเกินค่า Threshold หรือไม่
    if cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD:
        status = "CRITICAL"
        print(f"[!] Warning: Resource limit exceeded! Triggering alerts...")

        # 1. บันทึกลง Database
        save_alert_to_db(timestamp, cpu, ram, status)

        # 2. ยิง Alert ผ่าน API
        send_api_alert(timestamp, cpu, ram)
    else:
        print("[+] System resources are operating within normal parameters.")


if __name__ == "__main__":
    check_system_and_alert()