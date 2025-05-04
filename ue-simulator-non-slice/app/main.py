import asyncio
import time
import httpx
import traceback

requests_sent = 0
latencies = []

async def ue_simulator(request_type, load_factor):
    request = {"type": request_type, "load_factor": load_factor}
    gateway_url = "http://api-gateway.non-slice.svc.cluster.local:8000/api/request"
    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=200.0) as client:
            response = await client.post(gateway_url, json=request)
        response.raise_for_status()
        latency = time.time() - start
        return response.json(), latency
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")
        traceback.print_exc()
        return None, None

async def send_requests_once(load_factor, frequency):
    global requests_sent
    request_types = ["registration", "session_establishment", "data_transfer"]
    tasks = [asyncio.create_task(ue_simulator(req_type, load_factor)) 
             for req_type in request_types for _ in range(frequency)]
    results = await asyncio.gather(*tasks)
    
    for res, latency in results:
        if latency is not None:
            latencies.append(latency)
            requests_sent += 1

async def run_test(test_name, config, rounds=3, delay_between_rounds=10):
    global requests_sent, latencies
    requests_sent = 0
    latencies = []

    print(f"\n🧪 Starting Test: {test_name}")

    for round_num in range(rounds):
        print(f"\n🚀 Test Round {round_num + 1}")
        await asyncio.gather(*[
            send_requests_once(conf["load_factor"], conf["frequency"])
            for conf in config
        ])
        await asyncio.sleep(delay_between_rounds)

    rps = requests_sent / (rounds * 3)  # 3 request types
    avg_latency = (sum(latencies) / len(latencies)) if latencies else 0
    print(f"\n✅ Test {test_name} COMPLETED:")
    print(f"Total Requests: {requests_sent}, RPS: {rps:.2f}, Avg Latency: {avg_latency:.3f}s")

async def main():
    normal_test = [
        {"load_factor": 1, "frequency": 18}
    ]
    await run_test("Non-Slicing Normal Load", normal_test)

if __name__ == "__main__":
    asyncio.run(main())
