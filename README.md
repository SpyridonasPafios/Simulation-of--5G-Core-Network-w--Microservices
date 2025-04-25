# UE Simulator with Microservices & Network Slicing

This project simulates a User Equipment (UE) interacting with microservices within distinct network slices via an API Gateway. The system includes the following components:

- **UE Simulator**: Simulates user equipment requests.
- **API Gateway**: Forwards requests to specific services based on routing logic.
- **Auth Service**: Handles authentication workflows.
- **Session Service**: Establishes and manages sessions.
- **Policy Service**: Enforces slice-specific policies.
- **Resource Service**: Allocates network or compute resources.
- **Data Service**: Manages data transfer sessions.

Each service can exist in different namespaces (e.g. `embb`, `massive-iot`, `urllc`) to simulate network slicing.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Setup and Deployment](#setup-and-deployment)  
4. [Running the System](#running-the-system)  
5. [Updates](#updates)  
6. [Re-Run](#re-run)  
7. [Network Slicing](#network-slicing)

---

## Prerequisites

Ensure the following are installed and working:

- **Docker**: [Get Docker](https://docs.docker.com/get-docker/)
- **Minikube**: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
- (Optional) **DockerHub Account** if pushing images

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

### 1. Build Docker Images

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

### 2. Deploy to Kubernetes

```bash
# Start Minikube
minikube start

# Apply network slice namespaces
kubectl apply -f slices/namespaces.yaml

# Deploy all services
kubectl apply -f api-gateway/api-gateway-deployment.yaml
kubectl apply -f auth-service/auth-service-deployment.yaml
kubectl apply -f session-service/session-service-deployment.yaml
kubectl apply -f policy-service/policy-service-deployment.yaml
kubectl apply -f resource-service/resource-service-deployment.yaml
kubectl apply -f data-service/data-service-deployment.yaml
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
```

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

### Delete All (optional clean state)

```bash
kubectl delete pods --all
kubectl delete job --all
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

---
