const express = require('express');
const app = express();
const PORT = 3000;

// จำลองการเตรียมระบบ (เช่น การเชื่อมต่อ Database/Cache) ใช้เวลา 10 วินาที
let isReady = false;
setTimeout(() => {
  isReady = true;
  console.log("App is fully initialized and READY!");
}, 10000);

// Liveness Probe: เช็กว่า Process Node.js ยังไม่พัง/ไม่ค้าง
app.get('/health/live', (req, res) => {
  res.status(200).send('ALIVE');
});

// Readiness Probe: เช็กว่าพร้อมรับ Request หรือยัง
app.get('/health/ready', (req, res) => {
  if (isReady) {
    res.status(200).send('READY');
  } else {
    res.status(503).send('INITIALIZING');
  }
});

// Business Logic Route
const handleUserRequest = (req, res) => {
  res.json({
    status: "success",
    service: "Node.js User Service",
    version: "v1.1",
    data: {
      id: 101,
      username: "devops_engineer",
      role: "Cloud Specialist"
    }
  });
};

app.get('/', handleUserRequest);
app.get('/api/user', handleUserRequest);

app.listen(PORT, () => {
  console.log(`Node.js Service running on port ${PORT}`);
});