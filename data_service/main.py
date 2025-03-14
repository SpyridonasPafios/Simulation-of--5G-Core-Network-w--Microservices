from fastapi import FastAPI
import os

data_service = FastAPI()

@data_service.post("/forward_data")
async def forward_data(request: dict):
    stress_cpu(4, request.get("load_factor", 1))
    stress_ram(3, request.get("load_factor", 1))
    return {"status": "data_forwarded"}

@data_service.get("/health")
async def health_check():
    return {"status": "healthy"}