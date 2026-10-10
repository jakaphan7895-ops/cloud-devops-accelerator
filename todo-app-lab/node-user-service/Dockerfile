# 1. ใช้ Node.js Lightweight Image
FROM node:20-alpine

# 2. ตั้ง Working Directory
WORKDIR /app

# 3. ก๊อปปี้ package.json แล้วลง Dependencies
COPY package*.json ./
RUN npm install --only=production

# 4. ก๊อปปี้ source code ทั้งหมด
COPY . .

# 5. เปิด Port 3000 และสั่งรัน App
EXPOSE 3000
CMD ["npm", "start"]