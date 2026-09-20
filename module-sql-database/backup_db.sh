#!/bin/bash

# กำหนดชื่อไฟล์และโฟลเดอร์สำรองข้อมูล
DB_FILE="app_logs.db"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_${TIMESTAMP}.sqlite"

# สร้างโฟลเดอร์ backups ถ้ายังไม่มี
mkdir -p $BACKUP_DIR

# ตรวจสอบว่ามีไฟล์ DB อยู่จริงหรือไม่
if [ -f "$DB_FILE" ]; then
    cp $DB_FILE "${BACKUP_DIR}/${BACKUP_NAME}"
    echo "[SUCCESS] Database backed up to ${BACKUP_DIR}/${BACKUP_NAME}"
else
    echo "[ERROR] Database file $DB_FILE does not exist!"
    exit 1
fi