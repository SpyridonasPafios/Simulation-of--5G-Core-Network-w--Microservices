# 5G Microservices Simulation

This project simulates a **5G Core Network** using a **microservices-based architecture**. It includes an **API Gateway**, multiple **microservices**, and a **UE Simulator** to generate requests and measure performance.

## 🚀 Features
- Microservices for **Authentication, Session Management, Policy Control, Resource Management, and Data Forwarding**.
- **CPU/RAM stress testing** based on request load.
- **Network Slicing** with Kubernetes namespaces.
- Performance testing using a **UE Simulator**.

## 📌 Requirements
- **Python 3.8+**
- **FastAPI** & **Uvicorn**
- **Docker** & **Kubernetes** (for deployment)

## 🔧 Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/5g-microservices.git
   cd 5g-microservices
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## 🏃 Running the Microservices

Run each service in a separate terminal:

### API Gateway
```sh
uvicorn 5g_microservices:gateway --host 0.0.0.0 --port 8000 --reload
```

### Authentication Service
```sh
uvicorn 5g_microservices:auth_service --host 0.0.0.0 --port 8001 --reload
```

### Session Manager
```sh
uvicorn 5g_microservices:session_service --host 0.0.0.0 --port 8002 --reload
```

### Policy Control Service
```sh
uvicorn 5g_microservices:policy_service --host 0.0.0.0 --port 8003 --reload
```

### Resource Manager
```sh
uvicorn 5g_microservices:resource_service --host 0.0.0.0 --port 8004 --reload
```

### Data Forwarding Service
```sh
uvicorn 5g_microservices:data_service --host 0.0.0.0 --port 8005 --reload
```

## 📡 Running the UE Simulator

The UE Simulator sends requests and measures latency:
```sh
python 5g_microservices.py
```

## 📊 Testing API Requests
You can send requests manually using **cURL**:
```sh
curl -X POST "http://localhost:8000/api/request" \
-H "Content-Type: application/json" \
-d '{"type": "registration", "load_factor": 3}'
```

## 🐳 Running with Docker

1. **Build Docker images:**
   ```sh
   docker-compose build
   ```

2. **Run the services:**
   ```sh
   docker-compose up
   ```

## ☁️ Deploying on Kubernetes

1. **Apply Kubernetes manifests:**
   ```sh
   kubectl apply -f k8s/
   ```
2. **Check running pods:**
   ```sh
   kubectl get pods -n 5g-network
   ```

## 📈 Performance Monitoring

- **Latency comparison (slicing vs non-slicing).**
- **CPU/RAM utilization per namespace.**
- **Request rate per slice.**

## 🤝 Contributing
Feel free to open issues and pull requests! 🚀

## 📜 License
MIT License. See `LICENSE` file for details.
