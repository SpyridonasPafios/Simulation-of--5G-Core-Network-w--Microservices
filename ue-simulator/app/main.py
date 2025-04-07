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
    for i in range(1,6):
        for req_type in ["registration", "session_establishment", "data_transfer"]:
            load_factor = i
            result, latency = ue_simulator(req_type, load_factor)
            if latency:
             results.append((req_type, load_factor, latency))
    

    # Print summary
    if results:
        # Print summary with averages per load factor
        from collections import defaultdict
        load_factor_results = defaultdict(list)
        
        for req_type, load_factor, latency in results:
            load_factor_results[load_factor].append((req_type, latency))
        
        # Print per load factor
        for load_factor in sorted(load_factor_results.keys()):
            print(f"\nLoad Factor: {load_factor}")
            total_latency = 0
            
            for req_type, latency in load_factor_results[load_factor]:
                print(f"Request: {req_type}, Latency: {latency:.3f}s")
                total_latency += latency
            
            avg_latency = total_latency / len(load_factor_results[load_factor])
            print(f"Average Latency for Load Factor {load_factor}: {avg_latency:.3f}s")
        
        # Print overall average
        overall_avg = sum(latency for _, _, latency in results) / len(results)
        print(f"\nOverall Average Latency: {overall_avg:.3f}s")