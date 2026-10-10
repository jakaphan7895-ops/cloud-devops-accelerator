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

# 🔒 Lab 2: Kubernetes Secret Management & TLS/HTTPS Enforcer

This repository demonstrates how to secure edge traffic on a local Kubernetes cluster (`kind`) by implementing **TLS termination**, **Secret management**, and **automatic HTTP-to-HTTPS redirection** via the NGINX Ingress Controller.

---

## 🎯 Objectives
* Generate self-signed TLS certificates for local domain routing (`todo.local`).
* Store sensitive private keys and public certificates securely as **Kubernetes Secrets** (`kubernetes.io/tls`).
* Configure Ingress annotations to enforce secure connections and perform **Permanent Redirects (308)** from HTTP to HTTPS.

---

## 🛠️ Implementation Steps

### 1. Generating Self-Signed TLS Certificate
Created a private key (`tls.key`) and public certificate (`tls.crt`) for the domain `todo.local` using Docker[cite: 9]:

```PowerShell

docker run --rm -v ${PWD}:/work -w /work alpine/openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=todo.local/O=TodoApp"

```
### 2. Creating Kubernetes Secret
Packaged the certificate files into a secure Kubernetes Secret object:

```PowerShell

kubectl create secret tls todo-tls-secret --cert=tls.crt --key=tls.key

```

### 3. Ingress Manifest Configuration (k8s/app-ingress.yaml)
Configured the Ingress resource to reference the TLS secret and enforce strict HTTPS redirection:

```yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  annotations:
    # Enforce redirect from HTTP (port 80) to HTTPS (port 443)
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - todo.local
    secretName: todo-tls-secret
  rules:
  - host: todo.local
    http:
      paths:
      - path: /api/user
        pathType: Prefix
        backend:
          service:
            name: node-user-service
            port:
              number: 3000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-frontend-service
            port:
              number: 5000
```
🧪 Testing & Verification
Verifying HTTPS Traffic (TLS Termination):

```PowerShell
curl.exe -k [https://todo.local/api/user](https://todo.local/api/user)

Result: Successfully returned JSON response (status: success, role: Cloud Specialist) over port 443.

Verifying HTTP-to-HTTPS Redirection:

curl.exe -i [http://todo.local/api/user](http://todo.local/api/user)

Result: Returned HTTP/1.1 308 Permanent Redirect pointing to https://todo.local/api/user.
```
💡 Summary of Key Learnings

1.RollingUpdate Strategy: maxUnavailable: 0 ensures active instances handle traffic throughout deployment rollouts.

2.Graceful Shutdown: preStop lifecycle hooks prevent dropped connections while Ingress controllers unregister terminating pod endpoints.

3.Edge Security & TLS Termination: Offloading TLS decryption to Ingress reduces CPU overhead on downstream backend microservices.

4.Declarative Redirects: Utilizing Ingress annotations (ssl-redirect) standardizes security controls without application code changes.

# 📊 Lab 3: Prometheus & Grafana Monitoring Setup & Configuration

This lab covers the deployment, repository management, and advanced configuration of a complete Kubernetes monitoring stack using Helm, Prometheus, and Grafana.

---

## 📋 Overview
The goal of this lab is to establish observability, metrics collection, and visualization for Kubernetes workloads by deploying the **kube-prometheus-stack** Helm chart into a dedicated cluster environment.

---

## 🛠️ Step-by-Step Implementation

### 1. Helm Repository Setup
Before deploying the monitoring tools, the official Prometheus community Helm repository must be added and updated to fetch the latest chart versions:

```powershell
# Add the Prometheus community Helm repository
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)

# Update local Helm charts repository cache
helm repo update
```
### 2. Monitoring Stack Deployment
Deploy the entire monitoring bundle (including Prometheus, Grafana, Alertmanager, and exporters) into a custom namespace named monitoring:

```powershell
# Install kube-prometheus-stack with automated namespace creation
helm install monitoring-stack prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```
### 3. Local Access and Port Forwarding
Because internal cluster services are not exposed externally by default, kubectl port-forward is utilized to map the Grafana service to the local workstation:

```powershell
# Forward local port 3000 to Grafana's internal service port 80
kubectl port-forward svc/monitoring-stack-grafana -n monitoring 3000:80
```
⚙️ Advanced Configuration & Management
1. Customizing Helm Values
To override default configurations (such as storage retention, resource limits, or persistent volume claims), export or create a custom values.yaml file and apply it during installation:

```powershell
# Example of upgrading/modifying the release with a custom values file
helm upgrade monitoring-stack prometheus-community/kube-prometheus-stack --namespace monitoring -f values.yaml
```powershell
2. Inspecting Custom Resources (CRDs)
The kube-prometheus-stack installs several Custom Resource Definitions (CRDs) to manage monitoring objects declaratively, such as ServiceMonitors and PodMonitors:

```powershell
# List available monitoring custom resources
kubectl get servicemonitors -n monitoring
```powershell
3. Cleaning Up and Uninstallation
If the monitoring stack needs to be completely removed from the cluster, the Helm release can be uninstalled cleanly:

```powershell
# Uninstall the Helm release
helm uninstall monitoring-stack -n monitoring

# (Optional) Delete the monitoring namespace if no longer needed
kubectl delete namespace monitoring
```powershell