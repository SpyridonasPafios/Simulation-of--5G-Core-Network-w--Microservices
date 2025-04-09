import requests
import time
import random
import os
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def ue_simulator(request_type, load_factor, slice_type):
    request = {"type": request_type, "load_factor": load_factor, "slice": slice_type}
    start_time = time.time()
    try:
        namespace = slice_type  # Use the slice name directly for namespace
        gateway_url = f"http://api-gateway.{namespace}.svc.cluster.local:8000/api/request"
        print(f"[DEBUG] Sending request to: {gateway_url}")
        response = requests.post(gateway_url, json=request)
        response.raise_for_status()
        end_time = time.time()
        return slice_type, response.json(), end_time - start_time
    except Exception as e:
        print(f"[ERROR] Request failed for slice {slice_type}: {str(e)}")
        traceback.print_exc()
        return slice_type, None, None

if __name__ == "__main__":
    slice_types = {
        "embb": {"load_factor": 5, "frequency": 2},
        "massive-iot": {"load_factor": 1, "frequency": 10},
        "urllc": {"load_factor": 3, "frequency": 5}
    }

    # Use ThreadPoolExecutor to send concurrent requests
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_slice = []

        for slice_type, config in slice_types.items():
            for _ in range(config["frequency"]):
                future = executor.submit(
                    ue_simulator,
                    request_type="registration",
                    load_factor=config["load_factor"],
                    slice_type=slice_type
                )
                future_to_slice.append(future)

        for future in as_completed(future_to_slice):
            slice_type, result, latency = future.result()
            if latency is not None:
                print(f"✅ Slice: {slice_type}, Latency: {latency:.3f}s, Response: {result}")
            else:
                print(f"❌ Slice: {slice_type}, Request failed.")