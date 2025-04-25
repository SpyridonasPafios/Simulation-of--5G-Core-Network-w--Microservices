# UE Simulator with Microservices & Network Slicing

This project simulates **User Equipment (UE)** interacting with a suite of microservices through an API Gateway. Services are separated into **network slices** via Kubernetes namespaces (`embb`, `massive-iot`, `urllc`) to emulate 5G slicing behavior. The system includes integrated **observability with Prometheus & Grafana**.

Each service can exist in different namespaces (e.g. `embb`, `massive-iot`, `urllc`) to simulate network slicing.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Architecture Overview](#architecture-overview)  
3. [Project Structure](#project-structure)  
4. [Setup & Deployment](#setup--deployment)  
5. [Monitoring with Prometheus & Grafana](#monitoring-with-prometheus--grafana)  
6. [Running UE Simulation](#running-ue-simulation)  
7. [Test Tagging & Data Filtering](#test-tagging--data-filtering)  
8. [Cleaning Up](#cleaning-up)

---

## Prerequisites

Install the following before continuing:

- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm (for Grafana/Prometheus)](https://helm.sh/docs/intro/install/)
- (Optional) DockerHub account if pushing images

---

## Architecture Overview

```
+----------------+       +---------------+
|  UE Simulator  |-----> |  API Gateway  |----+
+----------------+       +---------------+    |
                                             \|/
                                     +---------------+
                                     |  Auth Service |
                                     +---------------+
                                     | Session Svc   |
                                     | Policy Svc    |
                                     | Resource Svc  |
                                     | Data Svc      |
                                     +---------------+

                Namespaced Slices: embb | massive-iot | urllc
```

Each slice operates in its own namespace and receives traffic via the gateway. Prometheus scrapes `/metrics` across all services, and Grafana provides dashboards to visualize:

- Request rates
- Average latency
- CPU usage per slice

---

## Project Structure

```
.
├── api-gateway/
│   ├── app/main.py
│   ├── Dockerfile
│   └── api-gateway-deployment.yaml
│
├── auth-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── auth-service-deployment.yaml
│
├── session-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── session-service-deployment.yaml
│
├── policy-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── policy-service-deployment.yaml
│
├── resource-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── resource-service-deployment.yaml
│
├── data-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── data-service-deployment.yaml
│
├── ue-simulator/
│   ├── app/main.py
│   ├── Dockerfile
│   └── ue-simulator-deployment.yaml
│
├── slices/
│   └── namespaces.yaml
│
├── monitoring/
│   └── monitor.yaml
|
└── README.md
```

---

## Setup and Deployment

### 1. Start Minikube

```bash
minikube start --memory=6144 --cpus=3
```

### 2. Install Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
```bash
kubectl create namespace monitoring
```
```bash
helm install prometheus-stack prometheus-community/kube-prometheus-stack \
  -f monitoring/prometheus-stack-values.yaml \
  -n monitoring --create-namespace
```

### 3. Build Docker Images

```bash
# Build API Gateway
cd api-gateway
docker build -t eliasandronikou/api-gateway .

# Build Auth Service
cd ../auth-service
docker build -t eliasandronikou/auth-service .

# Build Session Service
cd ../session-service
docker build -t eliasandronikou/session-service .

# Build Policy Service
cd ../policy-service
docker build -t eliasandronikou/policy-service .

# Build Resource Service
cd ../resource-service
docker build -t eliasandronikou/resource-service .

# Build Data Service
cd ../data-service
docker build -t eliasandronikou/data-service .

# Build UE Simulator
cd ../ue-simulator
docker build -t eliasandronikou/ue-simulator .
cd ..

```

### 4. Deploy to Kubernetes

```bash
# Apply network slice namespaces
kubectl apply -f slices/namespaces.yaml
kubectl apply -f monitoring/monitor.yaml

# Deploy all services
kubectl apply -f api-gateway/api-gateway-deployment.yaml
kubectl apply -f auth-service/auth-service-deployment.yaml
kubectl apply -f session-service/session-service-deployment.yaml
kubectl apply -f policy-service/policy-service-deployment.yaml
kubectl apply -f resource-service/resource-service-deployment.yaml
kubectl apply -f data-service/data-service-deployment.yaml
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
```

## 📊 Monitoring with Prometheus & Grafana

### 1. Access Grafana

```bash
kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80
```

Access Grafana at: [http://localhost:3000](http://localhost:3000)  
Default login:  
- **user**: `admin`  
- **pass**: `prom-operator` (or your defined value)

### 2. Import Dashboards

- Navigate to Grafana → Dashboards → Import
- Use dashboard IDs or JSON definitions (can be shared separately)


### 3. Verify Pods

```bash
kubectl get pods -A
```

---

## Running the System

UE Simulator will start sending requests on deploy. You can monitor logs:

```bash
kubectl logs -f <ue-simulator-pod-name>
```

---

## Updates

When making code changes:

### Delete

```bash
kubectl delete -f api-gateway/api-gateway-deployment.yaml
kubectl delete -f auth-service/auth-service-deployment.yaml
kubectl delete -f session-service/session-service-deployment.yaml
kubectl delete -f policy-service/policy-service-deployment.yaml
kubectl delete -f resource-service/resource-service-deployment.yaml
kubectl delete -f data-service/data-service-deployment.yaml
kubectl delete -f ue-simulator/ue-simulator-deployment.yaml
```

### 🧹 Delete All

To delete everything:

```bash
kubectl delete -f slices/namespaces.yaml
kubectl delete -f monitoring/monitor.yaml
kubectl delete deployments --all -n embb
kubectl delete deployments --all -n urllc
kubectl delete deployments --all -n massive-iot
helm uninstall prometheus-stack -n monitoring
```

To stop Minikube:

```bash
minikube stop
```

### Build & Push

```bash
# Build API Gateway
cd api-gateway
docker build -t eliasandronikou/api-gateway .
docker push eliasandronikou/api-gateway:latest
cd ..

# Build Auth Service
cd auth-service
docker build -t eliasandronikou/auth-service .
docker push eliasandronikou/auth-service:latest
cd ..

# Build Session Service
cd session-service
docker build -t eliasandronikou/session-service .
docker push eliasandronikou/session-service:latest
cd ..

# Build Policy Service
cd policy-service
docker build -t eliasandronikou/policy-service .
docker push eliasandronikou/policy-service:latest
cd ..

# Build Resource Service
cd resource-service
docker build -t eliasandronikou/resource-service .
docker push eliasandronikou/resource-service:latest
cd ..

# Build Data Service
cd data-service
docker build -t eliasandronikou/data-service .
docker push eliasandronikou/data-service:latest
cd ..

# Build UE Simulator
cd ue-simulator
docker build -t eliasandronikou/ue-simulator .
docker push eliasandronikou/ue-simulator:latest
cd ..

```

### Apply

```bash
kubectl apply -f api-gateway/api-gateway-deployment.yaml
kubectl apply -f auth-service/auth-service-deployment.yaml
kubectl apply -f session-service/session-service-deployment.yaml
kubectl apply -f policy-service/policy-service-deployment.yaml
kubectl apply -f resource-service/resource-service-deployment.yaml
kubectl apply -f data-service/data-service-deployment.yaml
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
kubectl apply -f monitoring/monitor.yaml

---

## Re-Run

To re-trigger UE simulation:

```bash
kubectl delete job ue-simulator
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
kubectl get pods
kubectl logs -f <ue-simulator-pod-name>
```

---

## Network Slicing

To observe services within each network slice:

```bash
kubectl get pods -n embb
kubectl get pods -n massive-iot
kubectl get pods -n urllc
```
```bash
#minikube
minikube start --memory=6144 --cpus=3
#Prometheus
minikube dashboard --url
#Grafana
kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80
```

---
