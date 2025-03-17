import requests
import time
import random

def ue_simulator(request_type, load_factor):
    request = {"type": request_type, "load_factor": load_factor}
    start_time = time.time()
    try:
        response = requests.post("http://api-gateway:8000/api/request", json=request)
        response.raise_for_status()
        end_time = time.time()
        return response.json(), end_time - start_time
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, None

if __name__ == "__main__":
    for req_type in ["registration", "session_establishment", "data_transfer"]:
        result, latency = ue_simulator(req_type, random.randint(1, 5))
        print(f"Request: {req_type}, Response: {result}, Latency: {latency:.3f}s" if latency else "Request failed")