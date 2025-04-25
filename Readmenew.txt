Here’s a fully enhanced `README.md` for your project, including Prometheus, Grafana, metrics filtering, and test isolation via labels. This version is structured, user-friendly, and provides all necessary steps for setup, monitoring, and testing in a Kubernetes + Minikube environment.

---

# 📡 UE Simulator with Microservices & Network Slicing

This project simulates **User Equipment (UE)** interacting with a suite of microservices through an API Gateway. Services are separated into **network slices** via Kubernetes namespaces (`embb`, `massive-iot`, `urllc`) to emulate 5G slicing behavior. The system includes integrated **observability with Prometheus & Grafana**.

---

## 📘 Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Architecture Overview](#architecture-overview)  
3. [Project Structure](#project-structure)  
4. [Setup & Deployment](#setup--deployment)  
5. [Monitoring with Prometheus & Grafana](#monitoring-with-prometheus--grafana)  
6. [Running UE Simulation](#running-ue-simulation)  
7. [Test Tagging & Data Filtering](#test-tagging--data-filtering)  
8. [Cleaning Up](#cleaning-up)

---

## ✅ Prerequisites

Install the following before continuing:

- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm (for Grafana/Prometheus)](https://helm.sh/docs/intro/install/)
- (Optional) DockerHub account if pushing images

---

## 📐 Architecture Overview

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

## 📁 Project Structure

```
.
├── api-gateway/
├── auth-service/
├── session-service/
├── policy-service/
├── resource-service/
├── data-service/
├── ue-simulator/
├── slices/
│   └── namespaces.yaml
├── monitoring/
│   ├── monitor.yaml
│   └── prometheus-stack-values.yaml
└── README.md
```

---

## 🚀 Setup & Deployment

### 1. Start Minikube

```bash
minikube start --memory=6144 --cpus=3
```

### 2. Install Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus-stack prometheus-community/kube-prometheus-stack \
  -f monitoring/prometheus-stack-values.yaml \
  -n monitoring --create-namespace
```

### 3. Build & Push Docker Images

Replace `<service-name>` with actual ones (or use the looped script):

```bash
cd <service-name>
docker build -t eliasandronikou/<service-name> .
docker push eliasandronikou/<service-name>
cd ..
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f slices/namespaces.yaml
kubectl apply -f monitoring/monitor.yaml

# Deploy services
kubectl apply -f api-gateway/api-gateway-deployment.yaml
kubectl apply -f auth-service/auth-service-deployment.yaml
kubectl apply -f session-service/session-service-deployment.yaml
kubectl apply -f policy-service/policy-service-deployment.yaml
kubectl apply -f resource-service/resource-service-deployment.yaml
kubectl apply -f data-service/data-service-deployment.yaml
kubectl apply -f ue-simulator/ue-simulator-deployment.yaml
```

---

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

> Pre-built queries include:
- 📈 `Request Rate per Slice`
- ⏱ `Average Latency per Slice`
- 🔧 `CPU Usage per Namespace`
- 🧪 `Filtered test_id views`

---

## 🧪 Running UE Simulation

To simulate traffic:

```bash
kubectl logs -f deployment/ue-simulator -n <slice>
```

Or run locally:

```bash
cd ue-simulator/app
python main.py
```

Simulation output includes per-slice:
- Request per second (RPS)
- Average latency

---

## 🏷 Test Tagging & Data Filtering

To isolate test runs in Prometheus/Grafana:

1. Add a `test_id` label to metrics (modify the `Instrumentator` in FastAPI apps):

```python
from prometheus_fastapi_instrumentator.metrics import Info

Instrumentator().add(
  Info(
    name="http_requests_total",
    description="...",
    labelnames=("test_id",),  # Add test_id here
    metric_namespace="custom"
  )
)
```

2. When making requests in your simulator, include:

```json
{
  "type": "registration",
  "slice": "embb",
  "load_factor": 5,
  "test_id": "run-001"
}
```

3. In Grafana, filter by `test_id="run-001"`.

---

## 🧹 Cleaning Up

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

---

## 📬 Questions?

Open an issue or reach out if you need help deploying or extending!

--- 

Let me know if you want a downloadable dashboard JSON too, or if you want to auto-deploy everything via a script or Helm chart 🚀