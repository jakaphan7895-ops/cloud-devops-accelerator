import datetime
import sqlite3


def init_db(db_name="app_logs.db"):
    """สร้าง Database และ Table สำหรับเก็บ System Logs"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # สร้าง Table เก็บการบันทึกสถานะ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"[+] Database '{db_name}' initialized successfully.")


def insert_log(event_type, message, db_name="app_logs.db"):
    """บันทึก Log ลง Database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO server_logs (timestamp, event_type, message)
        VALUES (?, ?, ?)
    """,
        (now, event_type, message),
    )

    conn.commit()
    conn.close()
    print(f"[+] Log inserted: [{event_type}] {message}")


def fetch_logs(db_name="app_logs.db"):
    """ดึงข้อมูล Log ทั้งหมดออกมาแสดงผล"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM server_logs ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()

    print("\n--- Latest 5 Logs ---")
    for row in rows:
        print(f"ID: {row[0]} | Time: {row[1]} | Type: {row[2]} | Message: {row[3]}")

    conn.close()


if __name__ == "__main__":
    init_db()

    # ทดสอบบันทึกข้อมูลแบบ Automate
    insert_log("INFO", "Server started successfully")
    insert_log("WARNING", "High CPU usage detected: 85%")
    insert_log("ERROR", "Failed SSH connection attempt from IP 192.168.1.100")

    # ดึงข้อมูลมาดู
    fetch_logs()