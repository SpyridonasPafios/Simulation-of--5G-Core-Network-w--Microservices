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
│   ├── requirements.txt         # Dependencies for API Gateway
│   └── api-gateway-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── auth-service/
│   ├── app/
│   │   └── main.py              # Python code for Authentication Service
│   ├── Dockerfile               # Dockerfile for Authentication Service
│   ├── requirements.txt         # Dependencies for Authentication Service
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
│   ├── requirements.txt         # Dependencies for Resource Manager
│   └── resource-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── data-service/
│   ├── app/
│   │   └── main.py              # Python code for Data Forwarding Service
│   ├── Dockerfile               # Dockerfile for Data Forwarding Service
│   ├── requirements.txt         # Dependencies for Data Forwarding Service
│   └── data-service-deployment.yaml  # Kubernetes Deployment and Service YAML
│
├── ue-simulator/
│   ├── app/
│   │   └── main.py              # Python code for UE Simulator
│   ├── Dockerfile               # Dockerfile for UE Simulator
│   ├── requirements.txt         # Dependencies for UE Simulator
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
cd ue-simulator
docker build -t your-username/ue-simulator:latest .
docker push your-username/ue-simulator:latest
```

### 2. Deploy UE Simulator

```bash
kubectl apply -f ue-simulator-job.yaml -n embb
kubectl apply -f ue-simulator-job.yaml -n massive-iot
kubectl apply -f ue-simulator-job.yaml -n urllc
```

### 3. View Logs

```bash
kubectl logs <ue-simulator-pod-name> -n embb
kubectl logs <ue-simulator-pod-name> -n massive-iot
kubectl logs <ue-simulator-pod-name> -n urllc
```

---

## Experiments

### Scenario A (Without Slicing)
- Deploy all microservices in a single namespace.
- Run the UE Simulator and measure latency.

### Scenario B (With Slicing)
- Deploy microservices in their respective namespaces (`embb`, `massive-iot`, `urllc`).
- Run the UE Simulator for each slice and measure latency.

---

## Results

Compare the latency measurements from **Scenario A** and **Scenario B** to analyze the impact of slicing on performance.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you need further assistance! 🚀