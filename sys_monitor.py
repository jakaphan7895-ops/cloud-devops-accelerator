import datetime
import os
import psutil


def get_system_metrics():
    # ดึงค่าเวลาปัจจุบัน
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ดึงค่า CPU, RAM และ Disk Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")

    # จัดรูปแบบข้อความ Log
    log_entry = (
        f"[{now}] "
        f"CPU: {cpu_usage}% | "
        f"RAM: {memory_info.percent}% | "
        f"Disk: {disk_info.percent}%\n"
    )

    return log_entry


def save_log(log_data, file_path="system_metrics.log"):
    # บันทึกข้อมูลลงไฟล์ (append mode)
    with open(file_path, "a") as f:
        f.write(log_data)
    print(f"Successfully wrote log to {file_path}")


if __name__ == "__main__":
    metrics = get_system_metrics()
    print("Collected Metrics:", metrics.strip())
    save_log(metrics)