from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import os

data_service = FastAPI()

# Prometheus metrics setup
Instrumentator().instrument(data_service).expose(data_service, endpoint="/metrics")

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
    
@data_service.post("/forward_data")
async def forward_data(request: dict):
    stress_cpu(4, request.get("load_factor", 1))
    stress_ram(3, request.get("load_factor", 1))
    return {"status": "data_forwarded"}

@data_service.get("/health")
async def health_check():
    return {"status": "healthy"}