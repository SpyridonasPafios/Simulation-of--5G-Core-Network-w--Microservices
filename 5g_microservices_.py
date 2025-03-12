from fastapi import FastAPI, HTTPException
import requests
import time
import random
import math
import os

# --- CPU & RAM Stress Functions ---
def compute_pi(n):
    pi = 0.0
    for k in range(n):
        pi += (1 / 16**k) * (4 / (8*k + 1) - 2 / (8*k + 4) - 1 / (8*k + 5) - 1 / (8*k + 6))
    return pi

def stress_cpu(cpu_load, load_factor):
    n = cpu_load * load_factor * int(os.getenv("CPU_MULTIPLIER", 1000))
    compute_pi(n)

def stress_ram(ram_load, load_factor):
    size = ram_load * load_factor * int(os.getenv("RAM_MULTIPLIER", 1000000))
    _ = bytearray(size)

# --- API Gateway ---
gateway = FastAPI()

MICROSERVICES = {
    "auth": "http://localhost:8001",
    "session": "http://localhost:8002",
    "policy": "http://localhost:8003",
    "resource": "http://localhost:8004",
    "data": "http://localhost:8005"
}

@gateway.post("/api/request")
async def handle_request(request: dict):
    request_type = request.get("type")
    load_factor = request.get("load_factor", 1)
    
    try:
        if request_type == "registration":
            auth_resp = requests.post(f"{MICROSERVICES['auth']}/authenticate", json=request).json()
            session_resp = requests.post(f"{MICROSERVICES['session']}/start_session", json=request).json()
            return {"auth": auth_resp, "session": session_resp}

        elif request_type == "session_establishment":
            session_resp = requests.post(f"{MICROSERVICES['session']}/start_session", json=request).json()
            policy_resp = requests.post(f"{MICROSERVICES['policy']}/apply_policy", json=request).json()
            resource_resp = requests.post(f"{MICROSERVICES['resource']}/allocate_resources", json=request).json()
            return {"session": session_resp, "policy": policy_resp, "resource": resource_resp}

        elif request_type == "data_transfer":
            data_resp = requests.post(f"{MICROSERVICES['data']}/forward_data", json=request).json()
            return {"data": data_resp}

        else:
            raise HTTPException(status_code=400, detail="Invalid request type")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Microservice error: {str(e)}")

# --- Authentication Service ---
auth_service = FastAPI()
@auth_service.post("/authenticate")
async def authenticate(request: dict):
    stress_cpu(3, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "authenticated"}

# --- Session Manager ---
session_service = FastAPI()
@session_service.post("/start_session")
async def start_session(request: dict):
    stress_cpu(3, request.get("load_factor", 1))
    stress_ram(3, request.get("load_factor", 1))
    return {"status": "session_started"}

# --- Policy Control Service ---
policy_service = FastAPI()
@policy_service.post("/apply_policy")
async def apply_policy(request: dict):
    stress_cpu(4, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "policy_applied"}

# --- Resource Manager ---
resource_service = FastAPI()
@resource_service.post("/allocate_resources")
async def allocate_resources(request: dict):
    stress_cpu(2, request.get("load_factor", 1))
    stress_ram(2, request.get("load_factor", 1))
    return {"status": "resources_allocated"}

# --- Data Forwarding Service ---
data_service = FastAPI()
@data_service.post("/forward_data")
async def forward_data(request: dict):
    stress_cpu(4, request.get("load_factor", 1))
    stress_ram(3, request.get("load_factor", 1))
    return {"status": "data_forwarded"}

# --- UE Simulator ---
def ue_simulator(request_type, load_factor):
    request = {"type": request_type, "load_factor": load_factor}
    start_time = time.time()
    try:
        response = requests.post("http://localhost:8000/api/request", json=request)
        response.raise_for_status()
        end_time = time.time()
        return response.json(), end_time - start_time
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None

if __name__ == "__main__":
    for req_type in ["registration", "session_establishment", "data_transfer"]:
        result, latency = ue_simulator(req_type, random.randint(1, 5))
        print(f"Request: {req_type}, Response: {result}, Latency: {latency:.3f}s" if latency else "Request failed")
