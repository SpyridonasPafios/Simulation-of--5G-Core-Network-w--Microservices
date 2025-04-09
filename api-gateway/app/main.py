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
    slice_type = request.get("slice", "embb")
    logger.info(f"[START] Received request: {request}")

    namespace = {
        "embb": "embb",
        "massive-iot": "massive-iot",
        "urllc": "urllc"
    }.get(slice_type, "embb")

    try:
        service_urls = {
            "auth": f"http://auth-service.{namespace}.svc.cluster.local:8001",
            "session": f"http://session-service.{namespace}.svc.cluster.local:8002",
            "policy": f"http://policy-service.{namespace}.svc.cluster.local:8003",
            "resource": f"http://resource-service.{namespace}.svc.cluster.local:8004",
            "data": f"http://data-service.{namespace}.svc.cluster.local:8005"
        }

        # Add stress (simulated load)
        logger.info("[LOAD] Stressing CPU and RAM")
        stress_cpu(1, load_factor)
        stress_ram(1, load_factor)

        # --- Request Flow ---
        if request_type == "registration":
            logger.info(f"[CALL] POST {service_urls['auth']}/authenticate")
            auth_resp = requests.post(f"{service_urls['auth']}/authenticate", json=request)
            logger.info(f"[RESP] Auth {auth_resp.status_code}: {auth_resp.text}")

            logger.info(f"[CALL] POST {service_urls['session']}/start_session")
            session_resp = requests.post(f"{service_urls['session']}/start_session", json=request)
            logger.info(f"[RESP] Session {session_resp.status_code}: {session_resp.text}")

            return {
                "auth": auth_resp.json(),
                "session": session_resp.json()
            }

        elif request_type == "session_establishment":
            logger.info(f"[CALL] POST {service_urls['session']}/start_session")
            session_resp = requests.post(f"{service_urls['session']}/start_session", json=request)
            logger.info(f"[RESP] Session {session_resp.status_code}: {session_resp.text}")

            logger.info(f"[CALL] POST {service_urls['policy']}/apply_policy")
            policy_resp = requests.post(f"{service_urls['policy']}/apply_policy", json=request)
            logger.info(f"[RESP] Policy {policy_resp.status_code}: {policy_resp.text}")

            logger.info(f"[CALL] POST {service_urls['resource']}/allocate_resources")
            resource_resp = requests.post(f"{service_urls['resource']}/allocate_resources", json=request)
            logger.info(f"[RESP] Resource {resource_resp.status_code}: {resource_resp.text}")

            return {
                "session": session_resp.json(),
                "policy": policy_resp.json(),
                "resource": resource_resp.json()
            }

        elif request_type == "data_transfer":
            logger.info(f"[CALL] POST {service_urls['data']}/forward_data")
            data_resp = requests.post(f"{service_urls['data']}/forward_data", json=request)
            logger.info(f"[RESP] Data {data_resp.status_code}: {data_resp.text}")

            return {"data": data_resp.json()}

        else:
            logger.warning("[ERROR] Invalid request type received.")
            raise HTTPException(status_code=400, detail="Invalid request type")

    except requests.exceptions.RequestException as e:
        logger.error(f"[EXCEPTION] Microservice request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Microservice error: {str(e)}")

    except Exception as e:
        logger.error(f"[EXCEPTION] General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
