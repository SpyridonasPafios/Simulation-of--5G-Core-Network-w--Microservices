# UE Simulator with Microservices

This project simulates a User Equipment (UE) interacting with a set of microservices via an API Gateway. The system includes the following components:

- **UE Simulator**: Simulates requests to the API Gateway.
- **API Gateway**: Routes requests to the appropriate microservices.
- **Auth Service**: Handles authentication requests.
- **Session Service**: Manages session establishment.
- **Policy Service**: Applies policies.
- **Resource Service**: Allocates resources.
- **Data Service**: Handles data transfer requests.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Setup and Deployment](#setup-and-deployment)
4. [Running the System](#running-the-system)
5. [Updates](#updates)
6. [Re-Run](#re-run)

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Kubernetes**: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/) or use a Kubernetes cluster.
- **kubectl**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## Project Structure

```
.
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
|
├── session-service/
│   ├── app/
│   │   └── main.py              # Python code for Session Manager
│   ├── Dockerfile               # Dockerfile for Session Manager
│   └── session-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── policy-service/
│   ├── app/
│   │   └── main.py              # Python code for Policy Control Service
│   ├── Dockerfile               # Dockerfile for Policy Control Service
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
│   └── ue-simulator-deployment.yaml  # Kubernetes Deployment and Service YAML
│
└── README.md                    # This file

```

---

## Setup and Deployment

### 1. Build Docker Images

Build Docker images for all services:

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

Deploy the services to your Kubernetes cluster:

```bash
# Start Minikube  
minikube start

# Deploy API Gateway
kubectl apply -f api-gateway/api-gateway-deployment.yaml

# Deploy Auth Service
kubectl apply -f auth-service/auth-service-deployment.yaml

# Deploy Session Service
kubectl apply -f session-service/session-service-deployment.yaml

# Deploy Policy Service
kubectl apply -f policy-service/policy-service-deployment.yaml

# Deploy Resource Service
kubectl apply -f resource-service/resource-service-deployment.yaml

# Deploy Data Service
kubectl apply -f data-service/data-service-deployment.yaml

# Deploy UE Simulator
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
```

### 3. Verify Deployment

Check that all pods are running:

```bash
kubectl get pods
kubectl get jobs
```

---

## Running the System

The `ue-simulator` will automatically start sending requests to the `api-gateway`. You can view the logs to see the results:

```bash
kubectl logs -f <ue-simulator-pod-name>
```

## Updates
For each Microservice that changed run Delete, then Build & Push and Apply. Finally go to [Re-Run](#re-run)

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

### Delete All
```bash
kubectl delete pods --all -n default
kubectl delete job --all
```

### Build & PUSH

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
```

## Re-Run

```bash
kubectl delete job ue-simulator
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
kubectl get pods
kubectl logs -f <ue-simulator-pod-name>
```