# 1. ใช้ Python 3.10 เวอร์ชันเล็ก (Alpine) เป็น Base Image
FROM python:3.10-alpine

# 2. ติดตั้ง system dependencies ที่จำเป็นสำหรับ psycopg2 (เอา --no-gradable ออก)
RUN apk add --no-cache gcc musl-dev postgresql-dev

# 3. กำหนด Directory การทำงานภายใน Container
WORKDIR /app

# 4. ก๊อปปี้ไฟล์โค้ดจากเครื่อง Host เข้าไปใน Container
COPY test_postgres.py .
COPY k8s/app.py .


# 5. ติดตั้ง Python Package ที่ต้องใช้
RUN pip install --no-cache-dir psycopg2-binary

RUN pip install flask psycopg2-binary

# 6. คำสั่งเริ่มต้นเมื่อ Container ทำงาน
CMD ["python", "app.py"]