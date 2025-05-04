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
        async with httpx.AsyncClient(timeout=100.0 if slice_type == "urllc" else 200.0) as client:
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

async def run_test(test_name, config, rounds=3, delay_between_rounds=10):
    global requests_sent, latency_per_slice
    requests_sent = {k: 0 for k in requests_sent}
    latency_per_slice = {k: [] for k in latency_per_slice}

    print(f"\n🧪 Starting Test: {test_name}")

    for round_num in range(rounds):
        print(f"\n🚀 Test Round {round_num + 1}")
        await asyncio.gather(*[
            send_requests_once(slice, conf["load_factor"], conf["frequency"])
            for slice, conf in config.items()
        ])
        await asyncio.sleep(delay_between_rounds)

    print(f"\n✅ Test {test_name} COMPLETED. Results:")
    for slice_type in requests_sent:
        rps = requests_sent[slice_type] / (rounds * 3)  # 3 request_types
        avg_latency = (
            sum(latency_per_slice[slice_type]) / len(latency_per_slice[slice_type])
            if latency_per_slice[slice_type]
            else 0
        )
        print(f"[{slice_type.upper()}] Total Requests: {requests_sent[slice_type]}, "
              f"RPS: {rps:.2f}, Avg Latency: {avg_latency:.3f}s")

async def main():
        # 🧪 Test : Normal load
    normal_test = {
        "embb": {"load_factor": 2, "frequency": 1},
        "massive-iot": {"load_factor": 1, "frequency": 10},
        "urllc": {"load_factor": 1, "frequency": 4}
    }
    await run_test("Normal Load Testing", normal_test)


if __name__ == "__main__":
    asyncio.run(main())