# 🚀 Lab 1: Kubernetes Zero-Downtime Deployment & Probes

This repository demonstrates how to achieve **Zero-Downtime Deployments** and robust application lifecycle management on a local Kubernetes cluster (`kind`) using **Readiness/Liveness Probes** and **Graceful Shutdown Strategies**.

---

## 🎯 Objectives
* Implement **Liveness** and **Readiness** probes for microservices.
* Configure zero-downtime `RollingUpdate` deployment strategies.
* Prevent race conditions (`502 Bad Gateway` / connection resets) during pod termination using `preStop` lifecycle hooks.
* Verify deployment reliability with continuous load testing scripts.

---

## 🏗️ Architecture & Configuration

### 1. Application Layer (`server.js`)
The Node.js application exposes health endpoints to reflect real-world initialization time (10-second startup delay):

* `/health/live`: Returns `200 OK` if the Node.js process is active.
* `/health/ready`: Returns `503 Service Unavailable` during startup, switching to `200 OK` once initialization completes.

### 2. Kubernetes Deployment (`k8s/node-user-deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-user-deployment
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Allow 1 temporary extra pod during updates
      maxUnavailable: 0  # Ensure zero unavailable pods during rollout
  selector:
    matchLabels:
      app: node-user-service
  template:
    metadata:
      labels:
        app: node-user-service
    spec:
      containers:
      - name: user-service
        image: node-user-service:v1.1
        ports:
        - containerPort: 3000
        
        # Lifecycle hook to resolve Ingress connection draining race condition
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]

        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 2
          periodSeconds: 3
          failureThreshold: 2

        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
```

🧪 Testing & Verification

Load Testing Script (PowerShell)
Executes continuous HTTP GET requests every 500ms to monitor traffic availability:

```PowerShell
while ($true) {
    try {
        $response = Invoke-RestMethod -Uri "[http://todo.local/api/user](http://todo.local/api/user)" -TimeoutSec 2
        Write-Host "$((Get-Date).ToString('HH:mm:ss')) - Success (Status: 200)" -ForegroundColor Green
    } catch {
        Write-Host "$((Get-Date).ToString('HH:mm:ss')) - FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
    Start-Sleep -MilliSeconds 500
}
```

Triggering Rollout

kubectl rollout restart deployment node-user-deployment

🔍 Troubleshooting & Key Learnings
Issue 1: Brief Request Drops During Rollout
Root Cause: Ingress controller routing tables retained terminating pod IP addresses for a split second before endpoints synced.

Resolution: Implemented lifecycle.preStop with a 5-second sleep to delay pod shutdown until the Ingress controller deregistered the endpoint.

Issue 2: 502 Bad Gateway Errors
Root Cause: Container process failure due to code execution errors (unhandled references) or missing K8s Service definitions.

Resolution: Debugged container logs using kubectl logs and verified Service endpoint availability via kubectl get endpoints.

💡 Technical Takeaways
RollingUpdate Strategy: Setting maxUnavailable: 0 ensures existing traffic is maintained while new replicas boot.

Probes vs Lifecycle: readinessProbe controls traffic routing, while livenessProbe manages container auto-healing.

Graceful Shutdown: preStop hooks are crucial in high-traffic environments to guarantee 100% Zero-Downtime deployments.

