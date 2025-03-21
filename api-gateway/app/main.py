from fastapi import FastAPI, HTTPException
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    "auth": "http://auth-service:8001",
    "session": "http://session-service:8002",
    "policy": "http://policy-service:8003",
    "resource": "http://resource-service:8004",
    "data": "http://data-service:8005"
}

@gateway.post("/api/request")
async def handle_request(request: dict):
    request_type = request.get("type")
    load_factor = request.get("load_factor", 1)
    logger.info(f"Received request: {request}")
    
    stress_cpu(1, load_factor)
    stress_ram(1, load_factor)

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
        logger.error(f"Microservice error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Microservice error: {str(e)}")

@gateway.get("/health")
async def health_check():
    return {"status": "healthy"}