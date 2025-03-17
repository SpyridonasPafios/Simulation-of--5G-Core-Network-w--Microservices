Here’s a comprehensive `README.md` file for your GitHub repository. This file explains the project, its structure, how to set it up, and how to run it. You can customize it further based on your specific needs.

---

# 5G Core Network Simulation with Kubernetes

This project simulates a 5G Core Network using microservices deployed in Kubernetes. It includes three network slices (eMBB, Massive IoT, and URLLC) with isolated resources and a UE Simulator to generate and measure requests.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Prerequisites](#prerequisites)
4. [Setup and Deployment](#setup-and-deployment)
5. [Running the UE Simulator](#running-the-ue-simulator)
6. [Experiments](#experiments)
7. [Results](#results)
8. [Contributing](#contributing)
9. [License](#license)

---

## Project Overview

The project simulates a 5G Core Network with the following components:

- **Microservices**:
  - API Gateway
  - Authentication Service
  - Session Manager
  - Policy Control Service
  - Resource Manager
  - Data Forwarding Service

- **Network Slices**:
  - **eMBB**: High load factor, fewer requests.
  - **Massive IoT**: Low load factor, frequent requests.
  - **URLLC**: Moderate load factor, low latency.

- **UE Simulator**:
  - Simulates user equipment (UE) requests for each slice.
  - Measures latency for different request types (registration, session establishment, data transfer).

---

## Folder Structure

```
5g-core-network/
├── api-gateway/
│   ├── app/
│   │   └── main.py              # Python code for API Gateway
│   ├── Dockerfile               # Dockerfile for API Gateway
│   └── api-gateway-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── auth-service/
│   ├── app/
│   │   └── main.py              # Python code for Authentication Service
│   ├── Dockerfile               # Dockerfile for Authentication Service
│   └── auth-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── session-service/
│   ├── app/
│   │   └── main.py              # Python code for Session Manager
│   ├── Dockerfile               # Dockerfile for Session Manager
│   ├── requirements.txt         # Dependencies for Session Manager
│   └── session-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── policy-service/
│   ├── app/
│   │   └── main.py              # Python code for Policy Control Service
│   ├── Dockerfile               # Dockerfile for Policy Control Service
│   ├── requirements.txt         # Dependencies for Policy Control Service
│   └── policy-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── resource-service/
│   ├── app/
│   │   └── main.py              # Python code for Resource Manager
│   ├── Dockerfile               # Dockerfile for Resource Manager
│   └── resource-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── data-service/
│   ├── app/
│   │   └── main.py              # Python code for Data Forwarding Service
│   ├── Dockerfile               # Dockerfile for Data Forwarding Service
│   └── data-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── ue-simulator/
│   ├── app/
│   │   └── main.py              # Python code for UE Simulator
│   ├── Dockerfile               # Dockerfile for UE Simulator
│   └── ue-simulator-job.yaml    # Kubernetes Job YAML for UE Simulator
│
├── embb-quota.yaml              # ResourceQuota for eMBB namespace
├── massive-iot-quota.yaml       # ResourceQuota for Massive IoT namespace
├── urllc-quota.yaml             # ResourceQuota for URLLC namespace
└── README.md                    # Project documentation
```

---

## Prerequisites

- **Docker**: Install Docker from [here](https://docs.docker.com/get-docker/).
- **Kubernetes**: Install Minikube or use a Kubernetes cluster.
- **kubectl**: Install kubectl from [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- **Python 3.9**: Install Python from [here](https://www.python.org/downloads/).

---

## Setup and Deployment

### 1. Build Docker Images

Navigate to each microservice folder and build the Docker image:

```bash
cd api-gateway
docker build -t your-username/api-gateway:latest .
docker push your-username/api-gateway:latest
```

Repeat for all microservices.

### 2. Create Kubernetes Namespaces

```bash
kubectl create namespace embb
kubectl create namespace massive-iot
kubectl create namespace urllc
```

### 3. Apply Resource Quotas

```bash
kubectl apply -f embb-quota.yaml
kubectl apply -f massive-iot-quota.yaml
kubectl apply -f urllc-quota.yaml
```

### 4. Deploy Microservices

Deploy microservices to their respective namespaces:

```bash
kubectl apply -f api-gateway-deployment-embb.yaml
kubectl apply -f auth-service-deployment-embb.yaml
# Repeat for all microservices and namespaces
```

---

## Running the UE Simulator

### 1. Build and Push UE Simulator Image

```bash
cd api-gateway
docker build -t eliasandronikou/api-gateway .
docker push eliasandronikou/api-gateway:latest
cd ..
cd auth-service
docker build -t eliasandronikou/auth-service .
docker push eliasandronikou/auth-service:latest
cd ..
cd session-service
docker build -t eliasandronikou/session-service .
docker push eliasandronikou/session-service:latest
cd ..
cd policy-service
docker build -t eliasandronikou/policy-service .
docker push eliasandronikou/policy-service:latest
cd ..
cd resource-service
docker build -t eliasandronikou/resource-service .
docker push eliasandronikou/resource-service:latest
cd ..
cd data-service
docker build -t eliasandronikou/data-service .
docker push eliasandronikou/data-service:latest
cd ..
cd ue-simulator
docker build -t eliasandronikou/ue-simulator .
docker push eliasandronikou/ue-simulator:latest
cd ..
```

### 2. Deploy UE Simulator

```bash
kubectl apply -f api-gateway/api-gateway-deployment.yaml
kubectl apply -f auth-service/auth-service-deployment.yaml
kubectl apply -f session-service/session-service-deployment.yaml
kubectl apply -f policy-service/policy-service-deployment.yaml
kubectl apply -f resource-service/resource-service-deployment.yaml
kubectl apply -f data-service/data-service-deployment.yaml
kubectl apply -f ue-simulator/ue-simulator.yaml
```

### 3. View Logs

```bash
kubectl get jobs
kubectl get pods
kubectl logs <pod-name>
```

### 4. Updates

```bash
docker build -t eliasandronikou/api-gateway:latest .
```
### 5. Clean ups

```bash
kubectl delete -f api-gateway-deployment.yaml
kubectl delete -f auth-service-deployment.yaml
kubectl delete -f session-service-deployment.yaml
kubectl delete -f policy-service-deployment.yaml
kubectl delete -f resource-service-deployment.yaml
kubectl delete -f data-service-deployment.yaml
kubectl delete -f ue-simulator.yaml
```

### 6. Usefull commands

```bash
kubectl delete pods --all -n default
kubectl delete job ue-simulator
```

```bash
kubectl rollout restart deployment/api-gateway
kubectl rollout restart deployment/auth-service
kubectl rollout restart deployment/data-service
kubectl rollout restart deployment/policy-service
kubectl rollout restart deployment/resource-service
kubectl rollout restart deployment/session-service
```
