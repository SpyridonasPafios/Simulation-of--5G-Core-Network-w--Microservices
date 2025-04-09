import requests
import time
import random
import traceback
from datetime import datetime

def ue_simulator(request_type, load_factor, slice_type):
    request = {"type": request_type, "load_factor": load_factor, "slice": slice_type}
    start_time = time.time()
    try:
        namespace = os.getenv("SLICE_TYPE", "embb")
        gateway_url = f"http://api-gateway.{namespace}.svc.cluster.local:8000/api/request"

        print(f"[DEBUG] Sending request to: {gateway_url}")

        response = requests.post(gateway_url, json=request)        response.raise_for_status()
        end_time = time.time()
        return response.json(), end_time - start_time
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    slice_types = {
        "embb": {"load_factor": 5, "frequency": 2},        # Βαρύ φορτίο, λίγα requests
        "massive-iot": {"load_factor": 1, "frequency": 10}, # Ελαφρύ φορτίο, πολλά requests
        "urllc": {"load_factor": 3, "frequency": 5}        # Μέτριο φορτίο, μέτρια requests
    }

    for slice_type, config in slice_types.items():
        for _ in range(config["frequency"]):
            result, latency = ue_simulator("registration", config["load_factor"], slice_type)
            print(f"Slice: {slice_type}, Response: {result}, Latency: {latency:.3f}s" if latency else "Request failed")
            time.sleep(1)  # Μικρή καθυστέρηση μεταξύ των requests