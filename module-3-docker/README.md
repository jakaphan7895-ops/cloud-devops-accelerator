# 🚀 Module 3: Microservices Infrastructure with Docker & Kubernetes (kind)

This repository contains hands-on labs and configurations for migrating a Python application connected to a PostgreSQL database from a local Docker environment to a local **Kubernetes (kind)** cluster.

🏗️ Architecture Overview
The application architecture consists of a persistent Python Web Service (Flask API) that interacts with a PostgreSQL database running inside a single-node Kubernetes cluster created with kind.

```text
[ Host Browser / cURL ]
           │
           │ (Port Forwarding / NodePort: 30001)
           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Kubernetes Cluster (kind)                                               │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ python-app-service (NodePort: 30001 / TargetPort: 5000)         │   │
│   └─────────────────────────────────────────┬───────────────────────┘   │
│                                             │                           │
│                                             ▼                           │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ python-app-deployment (Flask API)                               │   │
│   │  - ConfigMap: app-config (APP_ENV, LOG_LEVEL, APP_PORT)        │   │
│   │  - Secret: postgres-secret (DB_USER, DB_PASSWORD, DB_NAME)      │   │
│   └─────────────────────────────────────────┬───────────────────────┘   │
│                                             │                           │
│                                             │ (Internal DNS: postgres-service:5432)
│                                             ▼                           │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ postgres-service (ClusterIP: 5432)                              │   │
│   └─────────────────────────────────────────┬───────────────────────┘   │
│                                             │                           │
│                                             ▼                           │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ postgres-deployment (PostgreSQL 15)                             │   │
│   │  - PVC: postgres-pvc (Persistent Storage)                       │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

📁 Repository Structure

.
├── app.py                      # Python Flask Web Application
├── requirements.txt            # Python dependencies (flask, psycopg2-binary)
├── Dockerfile                  # Container definition for Python application
├── k8s/                        # Kubernetes Manifests
│   ├── app-configmap.yaml      # Non-sensitive configuration data
│   ├── postgres-secret.yaml    # Encoded sensitive DB credentials
│   ├── postgres-pvc.yaml       # Persistent Volume Claim for database storage
│   ├── postgres-deployment.yaml# PostgreSQL Stateful workload definition
│   ├── postgres-service.yaml   # Internal ClusterIP service for PostgreSQL
│   ├── python-app-deployment.yaml # Python Web Application deployment definition
│   └── python-app-service.yaml # External NodePort service for Python app
└── README.md                   # Project documentation
text```

🛠️ Prerequisites
Docker Desktop (with Kubernetes / kind enabled)

kubectl CLI installed

Git

🚀 Step-by-Step Deployment Guide
1. Build and Load Docker Image into kind
Since kind utilizes a dedicated containerd image store inside its Docker node, local images built on the host Docker Engine must be explicitly imported or referenced properly.

# Build the Python Flask application image
docker build -t my-python-app:latest .

# Import image directly into the kind node containerd store
docker save my-python-app:latest -o my-python-app.tar
docker cp my-python-app.tar kind-control-plane:/my-python-app.tar
docker exec -it kind-control-plane ctr -n k8s.io images import /my-python-app.tar
rm my-python-app.tar

2. Apply Kubernetes Manifests
Apply all Kubernetes manifests located in the k8s/ folder:

kubectl apply -f k8s/

3. Verify Deployment Status
Check that all Pods, Services, PVCs, and ConfigMaps are up and running:

kubectl get pods,svc,pvc,configmap,secret

Example Output:

NAME                                         READY   STATUS    RESTARTS   AGE
pod/postgres-deployment-5989bf755-vxs4l      1/1     Running   0          2h
pod/python-app-deployment-54b87c8f7f-cc5bb   1/1     Running   0          10m

NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes       ClusterIP   10.96.0.1               443/TCP          1d
service/postgres-service ClusterIP   10.96.0.42              5432/TCP         2h
service/python-app-svc   NodePort    10.96.150.12            5000:30001/TCP   10m

🧪 Accessing and Testing the Application
Option A: Via Port Forwarding (Recommended for Development)
Forward port 5000 from the local host directly to the Python application service:

kubectl port-forward svc/python-app-service 5000:5000

Open your browser or run cURL:

curl http://localhost:5000

Option B: Via NodePort Service
If your kind cluster mapping permits NodePort traffic, access the app directly at:

curl http://localhost:30001

💡 Key Engineering Takeaways & Troubleshooting
During the migration from Docker Compose to Kubernetes, several critical edge cases were identified and resolved:

1.ErrImageNeverPull / Image Store Isolation:

Root Cause: kind nodes use their own isolated containerd daemon, meaning images residing on the host Docker Engine are not natively accessible inside the cluster.

Fix: Loaded the image into containerd via ctr import or configured imagePullPolicy: IfNotPresent.

2.CrashLoopBackOff vs. Long-Running Processes:

Root Cause: Transitioning short-lived execution scripts into a Kubernetes Deployment causes continuous pod restarts upon script completion (Exit 0).

Fix: Refactored the batch script into an event-driven Flask HTTP Web Server running a continuous listener process on port 5000.

3.Internal Service Discovery:

Configured Kubernetes internal CoreDNS resolution allowing the Python application to seamlessly connect to PostgreSQL via postgres-service:5432.