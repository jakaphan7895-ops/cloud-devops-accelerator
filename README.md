# Module 1: Linux & Python System Automation

## Overview
This project demonstrates basic Linux administration and Python automation by collecting system metrics (CPU, RAM, Disk) and logging them to a file.

## Files
- `sys_monitor.py`: Python script to fetch and log system metrics using `psutil`.
- `run_monitor.sh`: Shell script to execute the monitoring process.
- `system_metrics.log`: Output log file.

## How to Run
1. Install dependencies: `pip install psutil`
2. Execute script: `./run_monitor.sh`

# Module 2: SQL Foundations & Database Automation

## 📌 Overview
This module demonstrates core relational database operations, automated data logging with Python, and Database Backup procedures designed for Cloud/DevOps infrastructure support.

## 🚀 Features
- **Database Initialization:** Auto-creates database schema for application server logs.
- **Data Insertion & Retrieval:** Python script interface for logging events and querying logs.
- **Automated Backup:** Bash script to create timestamped database backups.

## 📂 Project Structure

## 🧰 How to Run
1. Run database automation script:
   ```bash
   python db_automation.py

   Execute backup script:
2.Execute backup script:
Bash
./backup_db.sh

# Terraform EC2 Lab

โปรเจกต์นี้ใช้ Terraform สร้าง AWS EC2 พร้อม VPC, Public Subnet, Internet Gateway และ Security Group สำหรับเชื่อมต่อผ่าน SSH

## สิ่งที่สร้าง

- VPC: `10.0.0.0/16`
- Public Subnet: `10.0.1.0/24`
- Internet Gateway
- Route Table สำหรับ Internet
- Security Group เปิด SSH Port `22`
- EC2 Ubuntu 22.04
- ติดตั้ง Docker อัตโนมัติด้วย `user_data`
- สร้าง SSH Key Pair ด้วย Terraform

## สิ่งที่ต้องเตรียม

- AWS Account
- AWS CLI
- Terraform
- ตั้งค่า AWS Credentials แล้ว

ตรวจสอบการติดตั้ง:

```powershell
terraform version
aws sts get-caller-identity
```

## วิธีใช้งาน

เข้าสู่โฟลเดอร์โปรเจกต์:

```powershell
cd module2-terraform-ec2
```

เริ่มต้น Terraform:

```powershell
terraform init
```

ตรวจสอบแผนการสร้าง:

```powershell
terraform plan
```

สร้างทรัพยากร:

```powershell
terraform apply
```

พิมพ์ `yes` เพื่อยืนยัน

## ดู Public IP

```powershell
terraform output ec2_public_ip
```

ดู Private Key:

```powershell
terraform output -raw private_key_pem
```

สามารถบันทึกเป็นไฟล์ได้ด้วย PowerShell:

```powershell
terraform output -raw private_key_pem | Out-File -Encoding ascii demo.pem
```

ตั้งค่า Permission ของไฟล์บน Windows:

```powershell
icacls demo.pem /inheritance:r
icacls demo.pem /grant:r "$($env:USERNAME):(R)"
```

## เชื่อมต่อ EC2 ผ่าน SSH

```powershell
ssh -i .\demo.pem ubuntu@<EC2_PUBLIC_IP>
```

## ลบทรัพยากร

```powershell
terraform destroy
```

พิมพ์ `yes` เพื่อยืนยันการลบ

## คำเตือนด้านความปลอดภัย

- ไม่ควรเปิด SSH จาก `0.0.0.0/0` ในระบบจริง
- ไม่ควร commit ไฟล์ `demo.pem`
- ไม่ควร commit ไฟล์ `terraform.tfstate`
- ควรจำกัด SSH ให้เฉพาะ IP ที่จำเป็น

เพิ่มไฟล์เหล่านี้ใน `.gitignore`:

```gitignore
*.pem
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl
```