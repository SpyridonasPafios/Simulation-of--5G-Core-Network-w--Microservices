import requests
import time
import random
from datetime import datetime

def ue_simulator(request_type, load_factor):
    request = {"type": request_type, "load_factor": load_factor}
    start_time = time.time()
    try:
        response = requests.post("http://api-gateway:8000/api/request", json=request)
        response.raise_for_status()
        end_time = time.time()
        latency = end_time - start_time
        print(f"[{datetime.now()}] Request: {request_type}, Load Factor: {load_factor}, Response: {response.json()}, Latency: {latency:.3f}s")
        return response.json(), latency
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Request failed: {request_type}, Load Factor: {load_factor}, Error: {str(e)}")
        return {"error": str(e)}, None

if __name__ == "__main__":
    results = []
    for i in range(6):
        for req_type in ["registration", "session_establishment", "data_transfer"]:
            load_factor = random.randint(1, 5)
            result, latency = ue_simulator(req_type, load_factor)
            if latency:
             results.append((req_type, load_factor, latency))
    

    # Print summary
    if results:
        print("\n=== Summary ===")
        for req_type, load_factor, latency in results:
            print(f"Request: {req_type}, Load Factor: {load_factor}, Latency: {latency:.3f}s")
        avg_latency = sum(latency for _, _, latency in results) / len(results)
        print(f"Average Latency: {avg_latency:.3f}s")