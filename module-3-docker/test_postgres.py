import os
import psycopg2

# ข้อมูลการเชื่อมต่อ (ตรงกับที่เราตั้งไว้ใน docker run)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "devops_db")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASS = os.getenv("DB_PASS", "mypassword")


def test_connection():
    try:
        # เชื่อมต่อ PostgreSQL ใน Container
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        cursor = conn.cursor()

        # สร้าง Table ทดสอบ
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS container_logs (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Insert ข้อมูลทดสอบ
        cursor.execute(
            "INSERT INTO container_logs (message) VALUES (%s);",
            ("Hello from Python to PostgreSQL in Docker!",),
        )
        conn.commit()

        # Query ข้อมูลออกมาแสดงผล
        cursor.execute("SELECT * FROM container_logs;")
        rows = cursor.fetchall()

        print("Successfully connected to PostgreSQL Container!")
        print("Data in Database:", rows)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[-] Connection Error: {e}")


if __name__ == "__main__":
    test_connection()