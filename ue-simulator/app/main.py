import asyncio
import time
import httpx
import os
import traceback

requests_sent = {"embb": 0, "massive-iot": 0, "urllc": 0}
latency_per_slice = {"embb": [], "massive-iot": [], "urllc": []}

async def ue_simulator(request_type, load_factor, slice_type):
    request = {"type": request_type, "load_factor": load_factor, "slice": slice_type}
    namespace = os.getenv("SLICE_TYPE", slice_type)
    gateway_url = f"http://api-gateway.{namespace}.svc.cluster.local:8000/api/request"
    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=100.0) as client:
            response = await client.post(gateway_url, json=request)
        response.raise_for_status()
        end = time.time()
        latency = end - start
        return response.json(), latency
    except Exception as e:
        print(f"[ERROR][{slice_type}] Request failed: {str(e)}")
        traceback.print_exc()
        return None, None

async def send_requests_once(slice_type, load_factor, frequency):
    global requests_sent
    request_types = ["registration", "session_establishment", "data_transfer"]
    tasks = [asyncio.create_task(ue_simulator(req_type, load_factor, slice_type))for req_type in request_types for _ in range(frequency)]
    results = await asyncio.gather(*tasks)
    for res, latency in results:
        if latency is not None:
            latency_per_slice[slice_type].append(latency)
            requests_sent[slice_type] += 1

async def main():
    # Adjust these parameters
    test_rounds = 3
    config = {
        "embb": {"load_factor": 1, "frequency": 2},
        "massive-iot": {"load_factor": 1, "frequency": 5},
        "urllc": {"load_factor": 1, "frequency": 3}
    }

    for round_num in range(test_rounds):
        print(f"\n🚀 Starting test round {round_num + 1}")
        await asyncio.gather(*[
            send_requests_once(slice, conf["load_factor"], conf["frequency"])
            for slice, conf in config.items()
        ])
        await asyncio.sleep(1)  # short pause between rounds

    # Summary
    print("\n✅ TEST COMPLETED. Results:")
    for slice_type in requests_sent:
        rps = requests_sent[slice_type] / test_rounds
        avg_latency = sum(latency_per_slice[slice_type]) / len(latency_per_slice[slice_type]) if latency_per_slice[slice_type] else 0
        print(f"[{slice_type.upper()}] Total Requests: {requests_sent[slice_type]}, RPS: {rps:.2f}, Avg Latency: {avg_latency:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
